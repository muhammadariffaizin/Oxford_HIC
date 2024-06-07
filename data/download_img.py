import csv
import argparse
import os
import grequests
from tqdm import tqdm

def download_images(batch, save_path, num_workers=8):
    urls = []
    image_ids = []

    for row in batch:
        image_id = row['image_id']
        image_url = row['image_url']
        urls.append(image_url)
        image_ids.append(image_id)

    # using map
    rs = (grequests.get(url) for url in urls)
    
    for i, response in tqdm(grequests.imap_enumerated(rs, size=num_workers)):
        if response is None:
            print(f"Failed to download image {image_ids[i]}")
            continue
        # if status code is not 200, skip
        if response.status_code != 200:
            print(f"Failed to download image {image_ids[i]}")
            continue
        image_id = image_ids[i]
        image_path = os.path.join(save_path, f'{image_id}.jpg')
        with open(image_path, 'wb') as image_file:
            image_file.write(response.content)

def download_images_from_csv(file_path, save_path, batch_size=1000, num_workers=8):
    # Open the CSV file
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        
        # Skip the header
        next(reader)

        # split the download into batches of batch_size
        # to avoid running out of memory
        while True:
            batch = []
            try:
                for _ in range(batch_size):
                    row = next(reader)
                    batch.append(row)
            except StopIteration:
                break

            download_images(batch, save_path, num_workers)

def parse_args():
    parser = argparse.ArgumentParser(description='Download images from CSV file')
    parser.add_argument('--file_path', type=str, default='./hic_data/oxford_hic_image_info.csv')
    parser.add_argument('--save_path', type=str, default='./hic_data/images')
    parser.add_argument('--batch_size', type=int, default=10000)
    parser.add_argument('--num_workers', type=int, default=8)
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    # Create the save path if it doesn't exist
    if not os.path.exists(args.save_path):
        os.makedirs(args.save_path)
        
    download_images_from_csv(args.file_path, args.save_path, args.batch_size, args.num_workers)


if __name__ == '__main__':
    main()
import csv
import requests
import argparse
import os
import grequests

def download_images_from_csv(file_path, save_path):
    # Open the CSV file
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        
        # Skip the header
        next(reader)

        # using grequests to download images in parallel
        urls = []
        image_ids = []

        for row in reader:
            image_id = row['image_id']
            image_url = row['image_url']
            urls.append(image_url)
            image_ids.append(image_id)

        # using map
        rs = (grequests.get(url) for url in urls)
        responses = grequests.map(rs)
        
        for i, response in enumerate(responses):
            # if status code is not 200, skip
            if response.status_code != 200:
                print(f"Failed to download image {image_ids[i]}")
                continue
            image_id = image_ids[i]
            image_path = os.path.join(save_path, f'{image_id}.jpg')
            with open(image_path, 'wb') as image_file:
                image_file.write(response.content)
            print(f"Downloaded image {image_id} to {image_path}")

def parse_args():
    parser = argparse.ArgumentParser(description='Download images from CSV file')
    parser.add_argument('--file_path', type=str, default='./hic_data/oxford_hic_image_info.csv')
    parser.add_argument('--save_path', type=str, default='./hic_data/images')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    # Create the save path if it doesn't exist
    if not os.path.exists(args.save_path):
        os.makedirs(args.save_path)
        
    download_images_from_csv(args.file_path, args.save_path)


if __name__ == '__main__':
    main()
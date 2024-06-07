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

        # using imap enumerated
        rs = [grequests.get(u) for u in urls]
        for i, response in grequests.imap_enumerated(rs, size=15):
            image_id = image_ids[i]
            print(image_id)
            if response.status_code == 200:
                with open(f"{save_path}/{image_id}.jpg", "wb") as img_file:
                    img_file.write(response.content)
            else:
                print(f"Failed to download image from {urls[i]}")

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
import os
import requests
import zipfile
from tqdm import tqdm

DATA_URL = "https://www.unsw.adfa.edu.au/unsw-canberra-cyber/cybersecurity/ADFA-NB15-Datasets/UNSW-NB15.zip"
DATA_DIR = "data/raw/public/unsw-nb15/"
ZIP_PATH = "data/raw/public/UNSW-NB15.zip"

os.makedirs(DATA_DIR, exist_ok=True)

def download_file(url, dest):
    if os.path.exists(dest):
        print(f"File already exists: {dest}")
        return
    print(f"Downloading {url}...")
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    with open(dest, 'wb') as file, tqdm(
        desc=dest,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
    print(f"Downloaded to {dest}")

def extract_zip(zip_path, extract_to):
    print(f"Extracting {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted to {extract_to}")

def main():
    download_file(DATA_URL, ZIP_PATH)
    extract_zip(ZIP_PATH, DATA_DIR)
    print("UNSW-NB15 dataset is ready in:", DATA_DIR)

if __name__ == "__main__":
    main() 
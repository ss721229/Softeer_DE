import requests
from bs4 import BeautifulSoup
import gzip
import os
import shutil

url = "https://amazon-reviews-2023.github.io/"
res = requests.get(url)
html = res.text

soup = BeautifulSoup(html, 'html.parser')
links = soup.select('#grouped-by-category > div.table-wrapper.colwidths-auto.docutils.container > table > tbody td:nth-child(7) > p > a:nth-child(1)')
data_links = []
for link in links:
    data_links.append(link.get("href"))

data_dir = "/Users/admin/Desktop/Softeer_DE/data/aws_reviews"
down_dir = "/Users/admin/Desktop/Softeer_DE/data/aws_reviews/gz"
ext_dir = "/Users/admin/Desktop/Softeer_DE/data/aws_reviews/ext"

os.makedirs(data_dir, exist_ok=True)
os.makedirs(down_dir, exist_ok=True)
os.makedirs(ext_dir, exist_ok=True)

# 3. 다운로드 + 압축 해제
for link in data_links:
    gz_filename = os.path.basename(link)  # 예: Software_v1.json.gz
    json_filename = gz_filename.replace(".gz", "")  # 예: Software_v1.json

    gz_path = os.path.join(down_dir, gz_filename)
    extracted_path = os.path.join(ext_dir, json_filename)

    # 3-1. .gz 다운로드
    print(f"Downloading {gz_filename}...")
    with requests.get(link, stream=True) as r:
        with open(gz_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    # 3-2. 압축 해제
    print(f"Extracting {gz_filename} to {json_filename}...")
    with gzip.open(gz_path, 'rb') as f_in:
        with open(extracted_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    print(f"✅ Done: {json_filename}")

print("🎉 All files downloaded and extracted!")
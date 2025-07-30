import requests
from bs4 import BeautifulSoup
import gzip
import os
import shutil

url = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
res = requests.get(url)
html = res.text

soup = BeautifulSoup(html, 'html.parser')
links = soup.select('.faq-answers > table ul > li:nth-child(1) a')
data_links = []
for link in links:
    data_links.append(link.get("href"))

data_dir = "/Users/admin/Desktop/Softeer_DE/missions/W4/M2/spark-data/tlc_trip_record_data"

os.makedirs(data_dir, exist_ok=True)

# 3. 다운로드 + 압축 해제
for link in data_links:
    file_name = os.path.basename(link)
    file_path = os.path.join(data_dir, file_name)

    # 3-1. parquet 다운로드
    print(f"Downloading {file_name}...")
    with requests.get(link, stream=True) as r:
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print(f"✅ Done: {file_name}")

print("🎉 All files downloaded and extracted!")
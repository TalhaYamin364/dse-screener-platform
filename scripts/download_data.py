from pathlib import Path

import requests

DATA_DIR = Path("data/raw")

SOURCES = [
    {
        "name": "mendeley",
        "filename": "DSE_Data.csv",
        "listing_url": "https://data.mendeley.com/public-api/datasets/5mww8rb9td/files?folder_id=root&version=1",
    },
]


def get_file_info(source):
    response = requests.get(source["listing_url"], timeout=30)
    items = response.json()
    download_url = None
    expected_size = None
    for item in items:
        if item["filename"] == source["filename"]:
            download_url = item["content_details"]["download_url"]
            expected_size = item["size"]
    if download_url is None:
        raise ValueError("not found in the listing: " + source["filename"])
    return download_url, expected_size


def download_source(source):
    download_url, expected_size = get_file_info(source)
    path = DATA_DIR / source["filename"]
    if path.exists() and path.stat().st_size == expected_size:
        print(source["name"], "already downloaded and the size matches")
    else:
        print(source["name"], "downloading...")
        file_response = requests.get(download_url, timeout=60)
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        path.write_bytes(file_response.content)
        if path.stat().st_size != expected_size:
            raise ValueError("downloaded file has the wrong size: " + source["filename"])
        print(source["name"], "saved", path.stat().st_size, "bytes")


if __name__ == "__main__":
    for source in SOURCES:
        download_source(source)

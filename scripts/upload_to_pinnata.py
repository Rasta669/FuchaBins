from pathlib import Path
import requests
import os


def upload_to_pinata(file_path):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    file_name = file_path.split("/")[-1:][0]
    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
    }
    with Path(file_path).open("rb") as fp:
        image_file = fp.read()
        response = requests.post(
            url, files={"file": (file_name, image_file)}, headers=headers
        )
        print(f"yeay uploaded {file_name} to pinnata")
        print(response.json())

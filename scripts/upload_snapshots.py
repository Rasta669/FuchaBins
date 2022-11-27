from scripts.upload_to_ipfs import upload_to_ipfs
from scripts.upload_to_pinnata import upload_to_pinata


def upload_snapshots(data):
    image_file = f"./snapshots/{data}.png"
    upload_to_ipfs(image_file)
    upload_to_pinata(image_file)


def main():
    upload_snapshots("data1")
    upload_snapshots("data2")

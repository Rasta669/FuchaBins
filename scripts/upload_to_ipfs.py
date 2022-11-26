from brownie import FuchaNft, network
from pathlib import Path
from metadata.sample_metadata import sample_metadata_template
import os
import requests
import json

OPENSEA_URL = "https://testnets.opensea.io/assets/goerli/{}/{}"

breed_to_image_uri = {
    "FuchaProto": "https://ipfs.io/ipfs/QmThhsULrEnppySNbmMpn8gE7fk2ozFAeu8oYCdjmRVVC2?filename=FuchaProto.jpg",
    "FuchaTemboG": "https://ipfs.io/ipfs/QmciCypyogKkAdMFXcFUJxnYpPmiQgk4mTDWSX7BduXFgg?filename=FuchaTemboY.jpg",
    "FuchaTemboY": "https://ipfs.io/ipfs/QmSKMtre3TwQYkHY4UiRauJfgMMv3WjHvLcBq1vZgYzL9D?filename=FuchaTemboG.jpg",
}

breed_to_metadata_uri = {
    "FuchaProto": "https://ipfs.io/ipfs/QmPw2PSaE64Zy4Qpu4xpuZc8P9wDRBZ3uy6k7bzPUsPtVS?filename=0-FuchaProto.json",
    "FuchaTemboG": "https://ipfs.io/ipfs/Qmd7dszFi4tz9GcM4HF955moBvhBhYytv2AcTpyZhSk9oJ?filename=2-FuchaTemboG.json",
    "FuchaTemboY": "https://ipfs.io/ipfs/QmcqEkYEGqqzxzevZjQCBfh1i39Ep7yC44HU7kA8Y6YFZT?filename=1-FuchaTemboY.json",
}


def create_metadata(image_uri=None):
    fucha_collectible = FuchaNft[-1]
    no_of_fucha_nfts = fucha_collectible.tokenCounter()
    ##looping through all created collectibles
    for tokenId in range(no_of_fucha_nfts):
        ##getting the breed
        breed = fucha_collectible.tokenIdToBreed(tokenId)
        ##'./metadata/goerli/0-pug.json'
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{tokenId}-{breed}.json"
        )
        ##checking whether the medata_file name exists
        if Path(metadata_file_name).exists() == True:
            print(
                f"{metadata_file_name} file exists, delete the current one to override it!!"
            )
        else:
            print(f"Creating {metadata_file_name} file...")
            ##setting the breed_metadata to the template dictionary and overrting it with the breed info
            breed_metadata = sample_metadata_template
            breed_metadata["name"] = breed
            breed_metadata["description"] = f"3D model Nft of {breed} dustbin!"
            image_file_path = "./img/" + f"{breed}" + ".jpg"  ##'./img/pug.png'
            print(image_file_path)
            ##checking whether its allowed to upload to ipfs from the env variable so that it does not always upload to ipfs when this script is run
            if os.getenv("UPLOAD_TO_IPFS") == "true":
                image_uri = upload_to_ipfs(image_file_path)
                ##upload_to_pinata(image_file_path)
            else:
                if image_uri:
                    image_uri = image_uri
                else:
                    image_uri = breed_to_metadata_uri[breed]
            print(image_uri)
            breed_metadata["image"] = image_uri
            print(breed_metadata)
            ##saving the breed_metadata dict to the metadata file name in json format
            with open(metadata_file_name, "w") as file:
                json.dump(breed_metadata, file)
                file.close()
            if os.getenv("UPLOAD_TO_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)
            else:
                metadata_uri = breed_to_metadata_uri[breed]
                print(f"the metadata uri of the {breed} is {metadata_uri}")


def upload_to_ipfs(file_path):
    ##opening that file path passed as binary
    with Path(file_path).open("rb") as fp:
        image_file = fp.read()
        end_point = "/api/v0/add"
        ##ipfs_node obtained by running ipfs daemon to start your node
        ipfs_node = "http://127.0.0.1:5001"
        ##posting the image file to ipfs
        response = requests.post(ipfs_node + end_point, files={"file": image_file})
        ##grabbing the hash from the ipfs response.
        ipfs_hash = response.json()["Hash"]
        ##renaming ./metadata/goerli/0-pug.json to 0-pug.json
        image_file_name = file_path.split("/")[-1:][0]
        ##getting the image uri
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={image_file_name}"
        print(image_uri)
        return image_uri


def main():
    create_metadata()

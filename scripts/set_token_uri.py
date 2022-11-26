from brownie import FuchaNft, network
from scripts.upload_to_ipfs import breed_to_image_uri, breed_to_metadata_uri
from scripts.helpful_scripts import OPENSEA_URL, get_account, LOCAL_DEVELOPMENT_NETWORKS


def set_tokenUri(tokenId, fucha, tokenUri, account):
    tx = fucha.setTokenUri(tokenId, tokenUri, {"from": account})
    tx.wait(1)
    print(
        f"Yeah the token uri of {tokenId} in this fucha collection is {fucha.tokenURI(tokenId)}"
    )


def main():
    account = get_account(account_name="rastas")
    fucha = FuchaNft[-1]
    no_of_collectibles = fucha.tokenCounter()
    ##looping through all nft tokens created
    for tokenId in range(no_of_collectibles):
        breed = fucha.tokenIdToBreed(tokenId)
        metadata_uri = breed_to_image_uri[breed]
        print(metadata_uri)
        ##checking if the token uri of the selected breed exists
        if not fucha.tokenURI(tokenId).startswith("https://"):
            set_tokenUri(tokenId, fucha, metadata_uri, account)
        else:
            print(f"the token URI of {tokenId}-{breed} is {fucha.tokenURI(tokenId)}")
        print(
            f"Now You can view your nft on {OPENSEA_URL.format(fucha.address, tokenId)}"
        )

from brownie import FuchaNft
from scripts.helpful_scripts import get_account


def deploy_fucha():
    account = get_account(account_name="rastas")
    fucha = FuchaNft.deploy({"from": account})
    print("FuchaNft deployed!")
    return fucha, account


# this create method is flexible as to how much of each breed a creator wants to create and mint
def create_fucha(fucha, account, breed_index):
    breed = fucha.breed(breed_index)
    creation_tx = fucha.createNft(breed_index, {"from": account})
    creation_tx.wait(1)
    print("created fucha nft>>")


def main():
    fucha, account = deploy_fucha()
    create_fucha(fucha, account, 0)
    create_fucha(fucha, account, 1)
    create_fucha(fucha, account, 2)
    # set_tokenUri()

from brownie import (
    accounts,
    network,
    config,
)
from web3 import Web3

LOCAL_DEVELOPMENT_NETWORKS = ["development", "local-ganache"]
FORKED_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
OPENSEA_URL = "https://testnets.opensea.io/assets/goerli/{}/{}"


def get_account(index=None, account_name=None):
    if index:
        return accounts[index]
    if account_name:
        return accounts.load(account_name)
    if (
        network.show_active() in LOCAL_DEVELOPMENT_NETWORKS
        or network.show_active() in FORKED_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])

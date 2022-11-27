from scripts.deploy_and_create_nft import deploy_fucha, create_fucha
from scripts.helpful_scripts import LOCAL_DEVELOPMENT_NETWORKS
from brownie import network
import pytest


def test_create_nft():
    # arrange
    if network.show_active() not in LOCAL_DEVELOPMENT_NETWORKS:
        pytest.skip()
    fucha, account = deploy_fucha()
    # act
    create_fucha(fucha, account, 0)
    tokenCounter = fucha.tokenCounter()
    # assert
    assert tokenCounter == 1
    assert fucha.tokenIdToBreed(tokenCounter - 1) == "FuchaProto"

from brownie import network, FuchaNft
from scripts.deploy_and_create_nft import deploy_fucha, create_fucha
from scripts.helpful_scripts import LOCAL_DEVELOPMENT_NETWORKS
import pytest


def test_can_deploy_and_create_fucha():
    ##arrange
    if network.show_active() in LOCAL_DEVELOPMENT_NETWORKS:
        pytest.skip()
    ##act
    fucha, account = deploy_fucha()
    create_fucha(fucha, account, 0)
    tokenCounter = fucha.tokenCounter()
    ##assert
    assert tokenCounter == 1
    assert fucha.tokenIdToBreed(tokenCounter - 1) == "FuchaProto"

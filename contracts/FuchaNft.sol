// SPDX-License-Identifier: MIT
/*
This nft contract is mintable, burnable and can
be used for governace too, and also can keep track of all
nft holders
*/
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/cryptography/draft-EIP712.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/draft-ERC721Votes.sol";

contract FuchaNft is ERC721URIStorage, Ownable, EIP712, ERC721Votes {
    uint256 public tokenCounter;
    address fucha_owner;
    address[] public fucha_owners;
    string[] public breed = ["FuchaProto", "FuchaTemboY", "FuchaTemboG"]; // nft name to be minted based on this contracts collection, to be updated by contract owne
    mapping(uint256 => string) public tokenIdToBreed;
    event breedAssigned(string indexed breed, uint256);

    constructor() ERC721("fuchaNft", "MTK") EIP712("fuchaNft", "1") {}

    // breed_index will allow a creator to choose from the breed to create and mint from the breed array and the breed_index shall not be more than breed arr length
    function createNft(uint256 breed_index) public {
        require(breed_index < breed.length);
        fucha_owner = msg.sender;
        uint256 tokenId = tokenCounter;
        string memory breed_name = breed[breed_index];
        tokenIdToBreed[tokenId] = breed_name;
        emit breedAssigned(breed_name, tokenId);
        _safeMint(fucha_owner, tokenId);
        tokenCounter++;
        if (checkOwner(fucha_owner) == 0) {
            fucha_owners.push(fucha_owner);
        }
    }

    // this fx checks against replicates of the same owner address in the fucha_owners array
    function checkOwner(address nft_owner) public view returns (uint256) {
        uint256 fuchaIndex;
        for (uint256 i; i < fucha_owners.length; i++) {
            if (fucha_owners[i] == nft_owner) {
                fuchaIndex++;
            }
            if (fuchaIndex == 1) {
                break;
            }
        }
        return fuchaIndex;
    }

    // The following functions are overrides required by Solidity.

    function _afterTokenTransfer(
        address from,
        address to,
        uint256 tokenId,
        uint256 batchSize
    ) internal override(ERC721, ERC721Votes) {
        super._afterTokenTransfer(from, to, tokenId, batchSize);
    }

    function setTokenUri(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(msg.sender, tokenId) == true,
            "Sorry you aint the onwer of this tokenId.."
        );
        _setTokenURI(tokenId, _tokenURI);
    }

    function _burn(uint256 tokenId)
        internal
        override(ERC721, ERC721URIStorage)
    {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }
}

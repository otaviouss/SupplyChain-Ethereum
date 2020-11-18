pragma solidity 0.7.0;
pragma experimental ABIEncoderV2;

contract Insercao {

    string[] private hashes;

    constructor() payable {
        hashes.push("0");
    }

    function addInfo(string memory hash, bool access) external payable {
        require(access);
        hashes.push(hash);
    }

    function verificarInfo(string memory hash, uint256 quantInfo) external view returns(bool) {
        uint i = 0;
        for(i=quantInfo; i>0; i--) {
            if(keccak256(abi.encodePacked(hashes[i])) == keccak256(abi.encodePacked(hash))) {
                return true;
            }
        }
        return false;
    }

}
pragma solidity 0.6.4;
pragma experimental ABIEncoderV2;

contract Insercao {

    Dado[] private infos;
    uint private quant = 0;

    constructor() public payable {
        infos.push(Dado("0","0","0","0","0","0", 0x0000000000000000000000000000000000000000));
    }

    struct Dado {
        string hashInfo;
        string day;
        string time;
        string place;
        string code;
        string codeAnterior;
        address addrSensor;
    }

    function addInfo(string memory hash, string memory day, string memory time, string memory place, string memory code, string memory codeAnterior, address addrSensor, bool access) public {
        if(access) {
            infos.push(Dado(hash, day, time, place, code, codeAnterior, addrSensor));
            incrementCount();
        }
    }

    function verificarInfo(string memory code) public view returns(bool) {
        uint i = 0;
        for(i=quant; i>0; i--) {
            if(keccak256(abi.encodePacked(infos[i].code)) == keccak256(abi.encodePacked(code))) {
                return true;
            }
        }
        return false;
    }

    function rastreioProd(string memory codeFinal, uint quantidade) public view returns(string[] memory, string[] memory, string[] memory, string[] memory, address[] memory) {
        uint i;
        uint j = 1;
        string memory code = codeFinal;
        
        quantidade += 1;
        string[] memory rastreioHashInfo = new string[](quantidade);
        string[] memory rastreioDay = new string[](quantidade);
        string[] memory rastreioTime = new string[](quantidade);
        string[] memory rastreioPlace = new string[](quantidade);
        address[] memory rastreioAddrSensor = new address[](quantidade);

        rastreioHashInfo[0] = "0";
        rastreioDay[0] = "0";
        rastreioTime[0] = "0";
        rastreioPlace[0] = "0";

        for(i=quant; i>0; i--) {
            if(keccak256(abi.encodePacked(code)) != keccak256(abi.encodePacked("0")) && keccak256(abi.encodePacked(infos[i].code)) == keccak256(abi.encodePacked(code))) {
                rastreioHashInfo[j] = infos[i].hashInfo;
                rastreioDay[j] = infos[i].day;
                rastreioTime[j] = infos[i].time;
                rastreioPlace[j] = infos[i].place;
                rastreioAddrSensor[j] = infos[i].addrSensor;
                code = infos[i].codeAnterior;
                j += 1;
            }
        }

        return(rastreioHashInfo, rastreioDay, rastreioTime, rastreioPlace, rastreioAddrSensor); 
    }
    
    function incrementCount() internal {
        quant += 1;
    }

    function quantidadeInfos() public view returns(uint) {
        return(quant);
    }
}
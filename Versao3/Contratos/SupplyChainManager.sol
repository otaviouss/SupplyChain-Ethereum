pragma solidity 0.7.0;

contract SupplyChainManager {
    
    address public administrador;
    mapping(address => address) public usuarios;
    
    constructor() payable {
        administrador = msg.sender;
        usuarios[msg.sender] = msg.sender;
    }

    modifier onlyAdministrador() {
        require(msg.sender == administrador, "Apenas o administrador pode executar essa funcao.");
        _;
    }
    
    modifier onlyUsuario() {
        require(msg.sender == usuarios[msg.sender], "Apenas usuarios podem executar essa funcao.");
        _;
    }
    
    //event novoUsuario(address usuario);
    
    event novaInformacao(string hash);
    
    function addUsuario(address usuario) external payable onlyAdministrador {
        usuarios[usuario] = usuario;
        //emit novoUsuario(usuario);
    }
    
    function addInfo(string memory hash) external payable onlyUsuario {
        emit novaInformacao(hash);
    }

}
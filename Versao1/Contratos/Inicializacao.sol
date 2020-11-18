pragma solidity 0.6.4;

contract Inicializacao {
    address private administrador;
    Ator[] private usuarios;

    uint private quantUsuarios = 0;

    constructor() public payable {
        administrador = msg.sender;
        usuarios.push(Ator(administrador, "Admin"));
        quantUsuarios = quantUsuarios + 1;
    }

    struct Ator {
        address addr;
        string label;
    }

    modifier onlyAdministrador() {
        require(
            msg.sender == administrador,
            "Apenas o administrador pode executar essa função."
            );
        _;
    }
    
    function retornaUsuarios() public view returns(address[] memory) {
        uint i;
        address[] memory users = new address[](quantUsuarios);
        for(i=0; i<quantUsuarios; i++) {
            users[i] = usuarios[i].addr;
        }
        return users;
    }

    function addUsuario(address usuario, string memory label) public onlyAdministrador {
        usuarios.push(Ator(usuario, label));
        quantUsuarios = quantUsuarios + 1;
    }

    function verificarUsuario(address usuario) public view returns(bool) {
        uint i = 0;
        for(i=0;i<quantUsuarios;i++) {
            if(usuarios[i].addr == usuario) {
                return true;
            }
        }
        return false;
    }

    function quantidadeUsuarios() public view returns(uint) {
        return(quantUsuarios);
    }
}
pragma solidity 0.7.0;

contract Inicializacao {
    address[] private usuarios;

    constructor() payable {
        address administrador = msg.sender;
        usuarios.push(administrador);
    }

    modifier onlyAdministrador() {
        require(
            msg.sender == usuarios[0],
            "Apenas o administrador pode executar essa funcao."
            );
        _;
    }
    
    function addUsuario(address usuario) external payable onlyAdministrador {
        usuarios.push(usuario);
    }
    
    function retornaUsuarios(uint256 quantUsuarios) external view returns(address[] memory) {
        uint i;
        address[] memory users = new address[](quantUsuarios+1);
        for(i=0; i<=quantUsuarios; i++) {
            users[i] = usuarios[i];
        }
        return users;
    }

    function verificarUsuario(address usuario, uint256 quantUsuarios) external view returns(bool) {
        uint i = 0;
        for(i=0;i<quantUsuarios;i++) {
            if(usuarios[i] == usuario) {
                return true;
            }
        }
        return false;
    }

}
# Aplicação Python para utilização dos contratos Insercao_v1 e Inicializacao_v1
# numa rede Ethereum com mecanismo de consenso Proof of Authority
# utilizando thread única (Devido à falta de suporte da biblioteca Web3.py
# a múltiplas threads, é preferível a utilização dessa aplicação)

import random
import string
import time
import logging
import json
import threading
import sys

from web3 import Web3
from web3.middleware import geth_poa_middleware
from datetime import date

SUPPLY_CHAIN = "0"
SENHA = "123"

v = -1
cont = 1
enderecos = []
contratoInicializacao = ""
contratoInsercao = ""
web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

def aguardarEnter():
    global cont
    input('\n*** Pressione ENTER para parar! ***\n')
    cont = False

def salvarFila():
    global cont
    while(cont == True):
        logTxPool = logging.getLogger('logTxPool')
        dictionary = web3.geth.txpool.status()
        logTxPool.info(int(dictionary["pending"]), 16)
        time.sleep(1)

def conectarContrato():
    global web3
    global contratoInicializacao
    global contratoInsercao
    try:
        web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

        web3.eth.defaultAccount = web3.eth.accounts[0]

        #Contrato Incialização

        abi = json.loads('[{"inputs":[],"stateMutability":"payable","type":"constructor"},{"inputs":[{"internalType":"address","name":"usuario","type":"address"},{"internalType":"string","name":"label","type":"string"}],"name":"addUsuario","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"quantidadeUsuarios","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"retornaUsuarios","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"usuario","type":"address"}],"name":"verificarUsuario","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]')

        bytecode = '60806040526000600255336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550600160405180604001604052806000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020016040518060400160405280600581526020017f41646d696e000000000000000000000000000000000000000000000000000000815250815250908060018154018082558091505060019003906000526020600020906002020160009091909190915060008201518160000160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550602082015181600101908051906020019061015892919061016c565b505050600160025401600281905550610211565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106101ad57805160ff19168380011785556101db565b828001600101855582156101db579182015b828111156101da5782518255916020019190600101906101bf565b5b5090506101e891906101ec565b5090565b61020e91905b8082111561020a5760008160009055506001016101f2565b5090565b90565b61061b806102206000396000f3fe608060405234801561001057600080fd5b506004361061004c5760003560e01c80630e232a201461005157806336770c2d1461012c578063770655821461018b578063b6f44bcd146101a9575b600080fd5b61012a6004803603604081101561006757600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803590602001906401000000008111156100a457600080fd5b8201836020820111156100b657600080fd5b803590602001918460018302840111640100000000831117156100d857600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f820116905080830192505050505050509192919290505050610205565b005b610134610376565b6040518080602001828103825283818151815260200191508051906020019060200280838360005b8381101561017757808201518184015260208101905061015c565b505050509050019250505060405180910390f35b610193610459565b6040518082815260200191505060405180910390f35b6101eb600480360360208110156101bf57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610463565b604051808215151515815260200191505060405180910390f35b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16146102aa576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260338152602001806105b36033913960400191505060405180910390fd5b600160405180604001604052808473ffffffffffffffffffffffffffffffffffffffff16815260200183815250908060018154018082558091505060019003906000526020600020906002020160009091909190915060008201518160000160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550602082015181600101908051906020019061036392919061050d565b5050506001600254016002819055505050565b6060600060606002546040519080825280602002602001820160405280156103ad5781602001602082028036833780820191505090505b509050600091505b60025482101561045157600182815481106103cc57fe5b906000526020600020906002020160000160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681838151811061040a57fe5b602002602001019073ffffffffffffffffffffffffffffffffffffffff16908173ffffffffffffffffffffffffffffffffffffffff168152505081806001019250506103b5565b809250505090565b6000600254905090565b60008060009050600090505b600254811015610502578273ffffffffffffffffffffffffffffffffffffffff166001828154811061049d57fe5b906000526020600020906002020160000160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614156104f5576001915050610508565b808060010191505061046f565b60009150505b919050565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061054e57805160ff191683800117855561057c565b8280016001018555821561057c579182015b8281111561057b578251825591602001919060010190610560565b5b509050610589919061058d565b5090565b6105af91905b808211156105ab576000816000905550600101610593565b5090565b9056fe4170656e6173206f2061646d696e6973747261646f7220706f646520657865637574617220657373612066756ec3a7c3a36f2ea2646970667358221220f259f785736fd6fb7ac74a8121598c03493fea48b2a0efcb37e25d4e55ff70d764736f6c63430006040033'

        web3.eth.contract(abi=abi, bytecode=bytecode)

        tx_hash = "0xfb3e14222354ce8254c9136ea21ca88c3e3b8617f9eaa6828815959c7c914ebe"

        tx_receipt = web3.eth.getTransactionReceipt(tx_hash)

        contratoInicializacao = web3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=abi
        )

        #Contrato Inserção

        abi = json.loads('[{"inputs":[],"stateMutability":"payable","type":"constructor"},{"inputs":[{"internalType":"string","name":"hash","type":"string"},{"internalType":"string","name":"day","type":"string"},{"internalType":"string","name":"time","type":"string"},{"internalType":"string","name":"place","type":"string"},{"internalType":"string","name":"code","type":"string"},{"internalType":"string","name":"codeAnterior","type":"string"},{"internalType":"address","name":"addrSensor","type":"address"},{"internalType":"bool","name":"access","type":"bool"}],"name":"addInfo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"quantidadeInfos","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"codeFinal","type":"string"},{"internalType":"uint256","name":"quantidade","type":"uint256"}],"name":"rastreioProd","outputs":[{"internalType":"string[]","name":"","type":"string[]"},{"internalType":"string[]","name":"","type":"string[]"},{"internalType":"string[]","name":"","type":"string[]"},{"internalType":"string[]","name":"","type":"string[]"},{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"code","type":"string"}],"name":"verificarInfo","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]')

        bytecode = '6080604052600060015560006040518060e001604052806040518060400160405280600181526020017f300000000000000000000000000000000000000000000000000000000000000081525081526020016040518060400160405280600181526020017f300000000000000000000000000000000000000000000000000000000000000081525081526020016040518060400160405280600181526020017f300000000000000000000000000000000000000000000000000000000000000081525081526020016040518060400160405280600181526020017f300000000000000000000000000000000000000000000000000000000000000081525081526020016040518060400160405280600181526020017f300000000000000000000000000000000000000000000000000000000000000081525081526020016040518060400160405280600181526020017f30000000000000000000000000000000000000000000000000000000000000008152508152602001600073ffffffffffffffffffffffffffffffffffffffff1681525090806001815401808255809150506001900390600052602060002090600702016000909190919091506000820151816000019080519060200190620001da929190620002c5565b506020820151816001019080519060200190620001f9929190620002c5565b50604082015181600201908051906020019062000218929190620002c5565b50606082015181600301908051906020019062000237929190620002c5565b50608082015181600401908051906020019062000256929190620002c5565b5060a082015181600501908051906020019062000275929190620002c5565b5060c08201518160060160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550505062000374565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106200030857805160ff191683800117855562000339565b8280016001018555821562000339579182015b82811115620003385782518255916020019190600101906200031b565b5b5090506200034891906200034c565b5090565b6200037191905b808211156200036d57600081600090555060010162000353565b5090565b90565b6113af80620003846000396000f3fe608060405234801561001057600080fd5b506004361061004c5760003560e01c80635d7e9490146100515780636218b1fa14610081578063b356a00e1461009d578063f0b40726146100bb575b600080fd5b61006b60048036038101906100669190610c5d565b6100ef565b6040516100789190611151565b60405180910390f35b61009b60048036038101906100969190610c9e565b610199565b005b6100a561031d565b6040516100b2919061116c565b60405180910390f35b6100d560048036038101906100d09190610de0565b610327565b6040516100e69594939291906110db565b60405180910390f35b6000806000905060015490505b600081111561018e57826040516020016101169190611098565b604051602081830303815290604052805190602001206000828154811061013957fe5b906000526020600020906007020160040160405160200161015a91906110af565b604051602081830303815290604052805190602001201415610180576001915050610194565b8080600190039150506100fc565b60009150505b919050565b80156103135760006040518060e001604052808a81526020018981526020018881526020018781526020018681526020018581526020018473ffffffffffffffffffffffffffffffffffffffff168152509080600181540180825580915050600190039060005260206000209060070201600090919091909150600082015181600001908051906020019061022f929190610b25565b50602082015181600101908051906020019061024c929190610b25565b506040820151816002019080519060200190610269929190610b25565b506060820151816003019080519060200190610286929190610b25565b5060808201518160040190805190602001906102a3929190610b25565b5060a08201518160050190805190602001906102c0929190610b25565b5060c08201518160060160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055505050610312610b13565b5b5050505050505050565b6000600154905090565b606080606080606060008060019050606089905060018901985060608960405190808252806020026020018201604052801561037757816020015b60608152602001906001900390816103625790505b50905060608a6040519080825280602002602001820160405280156103b057816020015b606081526020019060019003908161039b5790505b50905060608b6040519080825280602002602001820160405280156103e957816020015b60608152602001906001900390816103d45790505b50905060608c60405190808252806020026020018201604052801561042257816020015b606081526020019060019003908161040d5790505b50905060608d6040519080825280602002602001820160405280156104565781602001602082028036833780820191505090505b5090506040518060400160405280600181526020017f30000000000000000000000000000000000000000000000000000000000000008152508560008151811061049c57fe5b60200260200101819052506040518060400160405280600181526020017f3000000000000000000000000000000000000000000000000000000000000000815250846000815181106104ea57fe5b60200260200101819052506040518060400160405280600181526020017f30000000000000000000000000000000000000000000000000000000000000008152508360008151811061053857fe5b60200260200101819052506040518060400160405280600181526020017f30000000000000000000000000000000000000000000000000000000000000008152508260008151811061058657fe5b602002602001018190525060015497505b6000881115610af2576040516020016105af906110c6565b60405160208183030381529060405280519060200120866040516020016105d69190611098565b60405160208183030381529060405280519060200120141580156106625750856040516020016106069190611098565b604051602081830303815290604052805190602001206000898154811061062957fe5b906000526020600020906007020160040160405160200161064a91906110af565b60405160208183030381529060405280519060200120145b15610ae4576000888154811061067457fe5b90600052602060002090600702016000018054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156107195780601f106106ee57610100808354040283529160200191610719565b820191906000526020600020905b8154815290600101906020018083116106fc57829003601f168201915b505050505085888151811061072a57fe5b60200260200101819052506000888154811061074257fe5b90600052602060002090600702016001018054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156107e75780601f106107bc576101008083540402835291602001916107e7565b820191906000526020600020905b8154815290600101906020018083116107ca57829003601f168201915b50505050508488815181106107f857fe5b60200260200101819052506000888154811061081057fe5b90600052602060002090600702016002018054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156108b55780601f1061088a576101008083540402835291602001916108b5565b820191906000526020600020905b81548152906001019060200180831161089857829003601f168201915b50505050508388815181106108c657fe5b6020026020010181905250600088815481106108de57fe5b90600052602060002090600702016003018054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156109835780601f1061095857610100808354040283529160200191610983565b820191906000526020600020905b81548152906001019060200180831161096657829003601f168201915b505050505082888151811061099457fe5b6020026020010181905250600088815481106109ac57fe5b906000526020600020906007020160060160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff168188815181106109ea57fe5b602002602001019073ffffffffffffffffffffffffffffffffffffffff16908173ffffffffffffffffffffffffffffffffffffffff168152505060008881548110610a3157fe5b90600052602060002090600702016005018054600181600116156101000203166002900480601f016020809104026020016040519081016040528092919081815260200182805460018160011615610100020316600290048015610ad65780601f10610aab57610100808354040283529160200191610ad6565b820191906000526020600020905b815481529060010190602001808311610ab957829003601f168201915b505050505095506001870196505b878060019003985050610597565b84848484849c509c509c509c509c5050505050505050509295509295909350565b60018060008282540192505081905550565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f10610b6657805160ff1916838001178555610b94565b82800160010185558215610b94579182015b82811115610b93578251825591602001919060010190610b78565b5b509050610ba19190610ba5565b5090565b610bc791905b80821115610bc3576000816000905550600101610bab565b5090565b90565b600081359050610bd981611334565b92915050565b600081359050610bee8161134b565b92915050565b600082601f830112610c0557600080fd5b8135610c18610c13826111b4565b611187565b91508082526020830160208301858383011115610c3457600080fd5b610c3f8382846112e1565b50505092915050565b600081359050610c5781611362565b92915050565b600060208284031215610c6f57600080fd5b600082013567ffffffffffffffff811115610c8957600080fd5b610c9584828501610bf4565b91505092915050565b600080600080600080600080610100898b031215610cbb57600080fd5b600089013567ffffffffffffffff811115610cd557600080fd5b610ce18b828c01610bf4565b985050602089013567ffffffffffffffff811115610cfe57600080fd5b610d0a8b828c01610bf4565b975050604089013567ffffffffffffffff811115610d2757600080fd5b610d338b828c01610bf4565b965050606089013567ffffffffffffffff811115610d5057600080fd5b610d5c8b828c01610bf4565b955050608089013567ffffffffffffffff811115610d7957600080fd5b610d858b828c01610bf4565b94505060a089013567ffffffffffffffff811115610da257600080fd5b610dae8b828c01610bf4565b93505060c0610dbf8b828c01610bca565b92505060e0610dd08b828c01610bdf565b9150509295985092959890939650565b60008060408385031215610df357600080fd5b600083013567ffffffffffffffff811115610e0d57600080fd5b610e1985828601610bf4565b9250506020610e2a85828601610c48565b9150509250929050565b6000610e408383610e60565b60208301905092915050565b6000610e588383610f82565b905092915050565b610e6981611299565b82525050565b6000610e7a82611215565b610e84818561125b565b9350610e8f836111e0565b8060005b83811015610ec0578151610ea78882610e34565b9750610eb283611241565b925050600181019050610e93565b5085935050505092915050565b6000610ed882611220565b610ee2818561126c565b935083602082028501610ef4856111f0565b8060005b85811015610f305784840389528151610f118582610e4c565b9450610f1c8361124e565b925060208a01995050600181019050610ef8565b50829750879550505050505092915050565b610f4b816112ab565b82525050565b6000610f5c82611236565b610f66818561128e565b9350610f768185602086016112f0565b80840191505092915050565b6000610f8d8261122b565b610f97818561127d565b9350610fa78185602086016112f0565b610fb081611323565b840191505092915050565b600081546001811660008114610fd85760018114610ffd57611041565b607f6002830416610fe9818761128e565b955060ff1983168652808601935050611041565b6002820461100b818761128e565b955061101685611200565b60005b8281101561103857815481890152600182019150602081019050611019565b82880195505050505b505092915050565b600061105660018361128e565b91507f30000000000000000000000000000000000000000000000000000000000000006000830152600182019050919050565b611092816112d7565b82525050565b60006110a48284610f51565b915081905092915050565b60006110bb8284610fbb565b915081905092915050565b60006110d182611049565b9150819050919050565b600060a08201905081810360008301526110f58188610ecd565b905081810360208301526111098187610ecd565b9050818103604083015261111d8186610ecd565b905081810360608301526111318185610ecd565b905081810360808301526111458184610e6f565b90509695505050505050565b60006020820190506111666000830184610f42565b92915050565b60006020820190506111816000830184611089565b92915050565b6000604051905081810181811067ffffffffffffffff821117156111aa57600080fd5b8060405250919050565b600067ffffffffffffffff8211156111cb57600080fd5b601f19601f8301169050602081019050919050565b6000819050602082019050919050565b6000819050602082019050919050565b60008190508160005260206000209050919050565b600081519050919050565b600081519050919050565b600081519050919050565b600081519050919050565b6000602082019050919050565b6000602082019050919050565b600082825260208201905092915050565b600082825260208201905092915050565b600082825260208201905092915050565b600081905092915050565b60006112a4826112b7565b9050919050565b60008115159050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b82818337600083830152505050565b60005b8381101561130e5780820151818401526020810190506112f3565b8381111561131d576000848401525b50505050565b6000601f19601f8301169050919050565b61133d81611299565b811461134857600080fd5b50565b611354816112ab565b811461135f57600080fd5b50565b61136b816112d7565b811461137657600080fd5b5056fea2646970667358221220a856c8214e169488d8aae08871f4c07a29c3045f7166fc0d153d3da35f0922c564736f6c63430006040033'

        web3.eth.contract(abi=abi, bytecode=bytecode)

        tx_hash = "0x4ea5c4371f2f9d76e958858dedc51b2a407f5ccb87ecf331f80c997e35aada71"

        tx_receipt = web3.eth.getTransactionReceipt(tx_hash)

        contratoInsercao = web3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=abi
        )
        return("Conectado aos contratos!")
    except:
        return("Não foi possível conectar aos contratos.")

def inserir():
    global web3
    global cont
    global enderecos

    #numAtual = contratoInsercao.functions.quantidadeInfos().call()
    numAtual = 1

    web3.geth.personal.unlockAccount(web3.eth.accounts[0], SENHA, 0)

    print('\nInserindo dados dos sensores')
    while cont == 1:
        info = ""
        dia = ""
        hora = ""
        local = ""
        codigo = ""
        codAnterior = ""
        addr = ""

        tokens = string.ascii_letters + string.digits
        info += "".join(random.choice(tokens) for a in range(30))

        start_dt = date.today().replace(day=1, month=1).toordinal()
        end_dt = date.today().toordinal()
        dia = date.fromordinal(random.randint(start_dt, end_dt))
        dia = str(dia)

        hora = time.strftime("%H:%M:%S", time.localtime())

        tokens = string.ascii_lowercase
        local = "".join(random.choice(tokens) for b in range(10))

        codigo = str(numAtual)
        codAnterior = str(numAtual-1)
        
        if((numAtual - 1) % 10 == 0):
            codAnterior = "0"

        tokens = string.digits
        addr = enderecos[int(random.choice(tokens))]

        try:
            valido = contratoInicializacao.functions.verificarUsuario(addr).call()

            if(valido):           
                aguardarInsercao(info, dia, hora, local, SUPPLY_CHAIN + "A" + codigo, SUPPLY_CHAIN + "A" + codAnterior, addr)
                
                print("Dado enviado com sucesso!", numAtual)
                numAtual += 1
            else:
                print("Usuário não cadastrado.")
        except:
            print("Endereço de Sensor Inválido")

        if cont == False:
            print('Finalizar')

def setup_logger(logger_name, log_file, level=logging.INFO):
    log_setup = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%H:%M:%S')
    fileHandler = logging.FileHandler(log_file, mode='a')
    fileHandler.setFormatter(formatter)
    log_setup.setLevel(level)
    log_setup.addHandler(fileHandler)

def aguardarInsercao(info, dia, hora, local, codigo, codAnterior, addr):
    startTime = time.perf_counter()
    
    nonce = web3.eth.getTransactionCount(web3.eth.accounts[0])
    transaction = contratoInsercao.functions.addInfo(info, dia, hora, local, codigo, codAnterior, addr, True).buildTransaction({'nonce': nonce})

    #Local do arquivo com a chave privada
    with open('D:\\Documentos\\IC\\Nodes\\Node3\\keystore\\UTC--2020-07-30T12-46-19.484613700Z--9be66d24bc51d99a6daaae0ed35108a9f6765751') as keyfile:
        encrypted_key = keyfile.read()
        private_key = web3.eth.account.decrypt(encrypted_key, SENHA)

    signed_tx = web3.eth.account.signTransaction(transaction, private_key)

    txn_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)  
    
    try:
        web3.eth.waitForTransactionReceipt(txn_hash, timeout=600)
        elapsed = time.perf_counter() - startTime
    except:
        elapsed = 0

    logTime = logging.getLogger('logTime')
    logTime.info(elapsed)

def gerarEnderecos():
    global web3
    global enderecos
    q = contratoInicializacao.functions.quantidadeUsuarios().call()

    print('\nGerando/Carregando Endereços')
    ends = contratoInicializacao.functions.retornaUsuarios().call()
    if(SUPPLY_CHAIN != "1" or len(ends) >= 10):
        while(len(ends)<10):
            time.sleep(2)
            ends = contratoInicializacao.functions.retornaUsuarios().call()
        
        for i in range(10):
            enderecos.append(ends[i])
        print('Endereços carregados com sucesso!')
    else:
        for i in range(10):
            nome = ""
            endereco = ""

            tokens = string.ascii_lowercase
            nome += "".join(random.choice(tokens) for y in range(10))

            tokens = string.digits
            endereco += "".join(random.choice(tokens) for z in range(40))

            web3.geth.personal.unlockAccount(web3.eth.accounts[0], SENHA)
            valid_address = web3.toChecksumAddress(endereco)
            enderecos.append(valid_address)

            aguardarEndereco(valid_address, nome)

        print('Endereços enviados com sucesso!')

def aguardarEndereco(valid_address, nome):
    nonce = web3.eth.getTransactionCount(web3.eth.accounts[0])
    transaction = contratoInicializacao.functions.addUsuario(valid_address, nome).buildTransaction({'nonce': nonce})

    #Local do arquivo com a chave privada
    with open('D:\\Documentos\\IC\\Nodes\\Node3\\keystore\\UTC--2020-07-30T12-46-19.484613700Z--9be66d24bc51d99a6daaae0ed35108a9f6765751') as keyfile:
        encrypted_key = keyfile.read()
        private_key = web3.eth.account.decrypt(encrypted_key, SENHA)

    signed_tx = web3.eth.account.signTransaction(transaction, private_key)

    txn_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    web3.eth.waitForTransactionReceipt(txn_hash)

def rastrearProduto():
    print('--- Rastreio de Produto ---')
    code = input('Código do Produto: ')
    quantidadeUsuarios = contratoInicializacao.functions.quantidadeUsuarios().call()
    retorno = contratoInsercao.functions.rastreioProd(code, quantidadeUsuarios).call()
    print(retorno)

for param in sys.argv :
    SUPPLY_CHAIN = str(param)

res = conectarContrato()
if(res == "Conectado aos contratos!"):
    print(res)
    print('\nSUPPLY_CHAIN ==', SUPPLY_CHAIN)

    setup_logger('logTxPool', 'PoA-TxPool' + str(SUPPLY_CHAIN))
    setup_logger('logTime', 'PoA-Time' + str(SUPPLY_CHAIN))
    gerarEnderecos()

    t1 = threading.Thread(target=inserir)
    t2 = threading.Thread(target=aguardarEnter)
    t3 = threading.Thread(target=salvarFila)
    t1.start()
    t2.start()
    t3.start()
    t2.join()
    t3.join()
else:
    print(res)
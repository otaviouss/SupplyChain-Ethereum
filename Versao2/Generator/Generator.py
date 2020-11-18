# Aplicação Python para geração aleatória de dados para os contratos Insercao_v2 e Inicializacao_v2
# numa rede Ethereum com mecanismo de consenso Proof of Work

import random
import string
import time
import logging
import json
import threading
import sys

from web3 import Web3
from datetime import date

SUPPLY_CHAIN = "0"
SENHA = "123"

v = -1
cont = True
enderecos = []
contratoInicializacao = ""
contratoInsercao = ""
web3 = Web3

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

        abi = json.loads('[{"inputs": [],"stateMutability": "payable","type": "constructor"},{"inputs": [{"internalType": "address","name": "usuario","type": "address"}],"name": "addUsuario","outputs": [],"stateMutability": "payable","type": "function"},{"inputs": [{"internalType": "uint256","name": "quantUsuarios","type": "uint256"}],"name": "retornaUsuarios","outputs": [{"internalType": "address[]","name": "","type": "address[]"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "usuario","type": "address"},{"internalType": "uint256","name": "quantUsuarios","type": "uint256"}],"name": "verificarUsuario","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "view","type": "function"}]')

        bytecode = '608060405260003390506000819080600181540180825580915050600190039060005260206000200160009091909190916101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550506104998061007c6000396000f3fe6080604052600436106100345760003560e01c80635ad0608014610039578063932c97a01461007d578063b5dd67c61461010d575b600080fd5b61007b6004803603602081101561004f57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff16906020019092919050505061017e565b005b34801561008957600080fd5b506100b6600480360360208110156100a057600080fd5b810190808035906020019092919050505061029f565b6040518080602001828103825283818151815260200191508051906020019060200280838360005b838110156100f95780820151818401526020810190506100de565b505050509050019250505060405180910390f35b34801561011957600080fd5b506101666004803603604081101561013057600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050610390565b60405180821515815260200191505060405180910390f35b6000808154811061018b57fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614610239576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260318152602001806104336031913960400191505060405180910390fd5b6000819080600181540180825580915050600190039060005260206000200160009091909190916101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b6060600060608367ffffffffffffffff811180156102bc57600080fd5b506040519080825280602002602001820160405280156102eb5781602001602082028036833780820191505090505b509050600091505b83821015610386576000828154811061030857fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681838151811061033f57fe5b602002602001019073ffffffffffffffffffffffffffffffffffffffff16908173ffffffffffffffffffffffffffffffffffffffff168152505081806001019250506102f3565b8092505050919050565b60008060009050600090505b82811015610426578373ffffffffffffffffffffffffffffffffffffffff16600082815481106103c857fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16141561041957600191505061042c565b808060010191505061039c565b60009150505b9291505056fe4170656e6173206f2061646d696e6973747261646f7220706f646520657865637574617220657373612066756e63616f2ea2646970667358221220f8be15d6920266500cacf78c2c89c618ea3d72a9c341730e71869535891dc48b64736f6c63430007000033'

        web3.eth.contract(abi=abi, bytecode=bytecode)

        tx_hash = "0xe1ffd1d5aaa3711134cbbb51fa805a178beae49f503e818cb79ab8af8bfc40d9"

        tx_receipt = web3.eth.getTransactionReceipt(tx_hash)

        contratoInicializacao = web3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=abi
        )

        #Contrato Inserção

        abi = json.loads('[{"inputs": [],"stateMutability": "payable","type": "constructor"},{"inputs": [{"internalType": "string","name": "hash","type": "string"},{"internalType": "bool","name": "access","type": "bool"}],"name": "addInfo","outputs": [],"stateMutability": "payable","type": "function"},{"inputs": [{"internalType": "string","name": "hash","type": "string"},{"internalType": "uint256","name": "quantInfo","type": "uint256"}],"name": "verificarInfo","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "view","type": "function"}]')

        bytecode = '6080604052600080600181540180825580915050600190039060005260206000200160006040518060400160405280600181526020017f300000000000000000000000000000000000000000000000000000000000000081525090919091509080519060200190610071929190610077565b50610114565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106100b857805160ff19168380011785556100e6565b828001600101855582156100e6579182015b828111156100e55782518255916020019190600101906100ca565b5b5090506100f391906100f7565b5090565b5b808211156101105760008160009055506001016100f8565b5090565b61058d806101236000396000f3fe6080604052600436106100295760003560e01c80636512b7861461002e5780639077b7f21461006b575b600080fd5b34801561003a57600080fd5b50610055600480360381019061005091906102e2565b610087565b6040516100629190610432565b60405180910390f35b6100856004803603810190610080919061028e565b610129565b005b600080600090508290505b600081111561011d57836040516020016100ac9190610404565b60405160208183030381529060405280519060200120600082815481106100cf57fe5b906000526020600020016040516020016100e9919061041b565b60405160208183030381529060405280519060200120141561010f576001915050610123565b808060019003915050610092565b60009150505b92915050565b8061013357600080fd5b60008290806001815401808255809150506001900390600052602060002001600090919091909150908051906020019061016e929190610173565b505050565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106101b457805160ff19168380011785556101e2565b828001600101855582156101e2579182015b828111156101e15782518255916020019190600101906101c6565b5b5090506101ef91906101f3565b5090565b5b8082111561020c5760008160009055506001016101f4565b5090565b60008135905061021f81610529565b92915050565b600082601f83011261023657600080fd5b81356102496102448261047a565b61044d565b9150808252602083016020830185838301111561026557600080fd5b6102708382846104e7565b50505092915050565b60008135905061028881610540565b92915050565b600080604083850312156102a157600080fd5b600083013567ffffffffffffffff8111156102bb57600080fd5b6102c785828601610225565b92505060206102d885828601610210565b9150509250929050565b600080604083850312156102f557600080fd5b600083013567ffffffffffffffff81111561030f57600080fd5b61031b85828601610225565b925050602061032c85828601610279565b9150509250929050565b61033f816104d1565b82525050565b6000610350826104bb565b61035a81856104c6565b935061036a8185602086016104f6565b80840191505092915050565b60008154600181166000811461039357600181146103b8576103fc565b607f60028304166103a481876104c6565b955060ff19831686528086019350506103fc565b600282046103c681876104c6565b95506103d1856104a6565b60005b828110156103f3578154818901526001820191506020810190506103d4565b82880195505050505b505092915050565b60006104108284610345565b915081905092915050565b60006104278284610376565b915081905092915050565b60006020820190506104476000830184610336565b92915050565b6000604051905081810181811067ffffffffffffffff8211171561047057600080fd5b8060405250919050565b600067ffffffffffffffff82111561049157600080fd5b601f19601f8301169050602081019050919050565b60008190508160005260206000209050919050565b600081519050919050565b600081905092915050565b60008115159050919050565b6000819050919050565b82818337600083830152505050565b60005b838110156105145780820151818401526020810190506104f9565b83811115610523576000848401525b50505050565b610532816104d1565b811461053d57600080fd5b50565b610549816104dd565b811461055457600080fd5b5056fea2646970667358221220837e356d2189d8a42bb4c0f4a6d850f5ac6d8dcc22abe2c30803f83e929de2af64736f6c63430007000033'

        web3.eth.contract(abi=abi, bytecode=bytecode)

        tx_hash = "0x332f79c849ba39f07b59c32b458e67194fbc9f460a517dae60637aa8e4e54a42"

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

    numAtual = 1

    web3.geth.personal.unlockAccount(web3.eth.accounts[0], SENHA, 0)

    print('\nInserindo dados dos sensores')
    while cont == True:
        hashInfo = ""
        addr = ""

        tokens = string.ascii_letters + string.digits
        hashInfo += "".join(random.choice(tokens) for a in range(30))

        tokens = string.digits
        addr = enderecos[int(random.choice(tokens))]

        try:
            valido = contratoInicializacao.functions.verificarUsuario(addr, 10).call()

            if(valido):           
                aguardarInsercao(hashInfo)
                
                print("Hash enviado com sucesso!", numAtual)
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

def aguardarInsercao(hashInfo):
    costEther = 0
    startTime = time.perf_counter()
    tx_hash = contratoInsercao.functions.addInfo(hashInfo, True).transact()
    
    logTxPool = logging.getLogger('logTxPool')
    dictionary = web3.geth.txpool.status()
    logTxPool.info(dictionary["pending"])
    
    try:
        web3.eth.waitForTransactionReceipt(tx_hash, timeout=600)
        elapsed = time.perf_counter() - startTime
        
        receipt = web3.eth.getTransactionReceipt(tx_hash)
        gas = receipt["gasUsed"]
        print(gas)
        price = web3.eth.gasPrice
        print(price)
        cost = gas*price
        print(cost)
        costEther = cost/1000000000000000000
        print(costEther)
    except:
        elapsed = 0

    logTxTime = logging.getLogger('logTxTime')
    logTxTime.info(elapsed)

    logTxCost = logging.getLogger('logTxCost')
    logTxCost.info(costEther)

def gerarEnderecos():
    global web3
    global enderecos
    
    print('\nGerando Endereços')
    for i in range(10):
        endereco = ""

        tokens = string.digits
        endereco += "".join(random.choice(tokens) for z in range(40))

        web3.geth.personal.unlockAccount(web3.eth.accounts[0], SENHA)
        valid_address = web3.toChecksumAddress(endereco)

        aguardarEndereco(valid_address)
        
        enderecos.append(valid_address)

    print('Endereços enviados com sucesso!')

def aguardarEndereco(valid_address):
    tx_hash = contratoInicializacao.functions.addUsuario(valid_address).transact()
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)

def rastrearProduto():
    print('--- Rastreio de Produto ---')
    code = input('Código do Produto: ')
    print("No banco de dados local")

# -- MAIN -- #

for param in sys.argv :
    SUPPLY_CHAIN = str(param)

res = conectarContrato()
if(res == "Conectado aos contratos!"):
    print(res)
    print('\nSUPPLY_CHAIN ==', SUPPLY_CHAIN)

    setup_logger('logTxPool', 'TxPool' + str(SUPPLY_CHAIN))
    setup_logger('logTxTime', 'TxTime' + str(SUPPLY_CHAIN))
    setup_logger('logTxCost', 'TxCost' + str(SUPPLY_CHAIN))
    gerarEnderecos()

    t1 = threading.Thread(target=inserir)
    t2 = threading.Thread(target=aguardarEnter)
    t1.start()
    t2.start()
    t2.join()
#   t3 = threading.Thread(target=salvarFila)
#   t3.start()
#   t3.join()
else:
    print(res)
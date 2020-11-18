# Aplicação Python para geração aleatória de dados utilizando o contrato SupplyChain
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
contrato = ""
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
    global contrato
    try:
        web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

        web3.eth.defaultAccount = web3.eth.accounts[0]

        #Contrato SupplYChainManager

        abi = json.loads('[{"inputs": [{"internalType": "string","name": "hash","type": "string"}],"name": "addInfo","outputs": [],"stateMutability": "payable","type": "function"},{"inputs": [{"internalType": "address","name": "usuario","type": "address"}],"name": "addUsuario","outputs": [],"stateMutability": "payable","type": "function"},{"inputs": [],"stateMutability": "payable","type": "constructor"},{"anonymous": false,"inputs": [{"indexed": false,"internalType": "string","name": "hash","type": "string"}],"name": "novaInformacao","type": "event"},{"inputs": [],"name": "administrador","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "","type": "address"}],"name": "usuarios","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"}]')

        bytecode = '6080604052336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555033600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555061058f806100d16000396000f3fe60806040526004361061003f5760003560e01c80630bf803e4146100445780635ad06080146100ff5780637062b97d14610143578063f6b91ea914610184575b600080fd5b6100fd6004803603602081101561005a57600080fd5b810190808035906020019064010000000081111561007757600080fd5b82018360208201111561008957600080fd5b803590602001918460018302840111640100000000831117156100ab57600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f8201169050808301925050505050505091929192905050506101ff565b005b6101416004803603602081101561011557600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610381565b005b34801561014f57600080fd5b506101586104a6565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34801561019057600080fd5b506101d3600480360360208110156101a757600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff1690602001909291905050506104ca565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16146102e2576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252602b81526020018061052f602b913960400191505060405180910390fd5b7f6f2ffbff20b5fc27dfca426d287b01ac3c19d64a937c50f6b5b762462cdb7cec816040518080602001828103825283818151815260200191508051906020019080838360005b83811015610344578082015181840152602081019050610329565b50505050905090810190601f1680156103715780820380516001836020036101000a031916815260200191505b509250505060405180910390a150565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614610425576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260318152602001806104fe6031913960400191505060405180910390fd5b80600160008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60016020528060005260406000206000915054906101000a900473ffffffffffffffffffffffffffffffffffffffff168156fe4170656e6173206f2061646d696e6973747261646f7220706f646520657865637574617220657373612066756e63616f2e4170656e6173207573756172696f7320706f64656d20657865637574617220657373612066756e63616f2ea264697066735822122059668e01b1c7ff57c096f733bc2fb121dba9a2f6f526662784959768fa2c205164736f6c63430007010033'

        web3.eth.contract(abi=abi, bytecode=bytecode)

        tx_hash = '0x769ceb433cb2ed84aa6963f760bd073150c7c08fa4e9ace69c2d65b4d65e004e'

        tx_receipt = web3.eth.getTransactionReceipt(tx_hash)

        contrato = web3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=abi
        )

        return("Conectado ao contrato!")
    except:
        return("Não foi possível conectar ao contrato.")

def inserir():
    global web3
    global cont
    global enderecos

    web3.geth.personal.unlockAccount(web3.eth.accounts[0], SENHA, 0)
    quant = 0

    print('\nInserindo dados dos sensores')
    while cont == True:
        info = ""

        tokens = string.ascii_letters + string.digits
        info += "".join(random.choice(tokens) for a in range(30))

        try:       
            aguardarInsercao(info)
            
            quant += 1
            print("Dado enviado com sucesso! ", quant)
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

def aguardarInsercao(info):
    costEther = 0
    startTime = time.perf_counter()
    tx_hash = contrato.functions.addInfo(info).transact()
    
    logTxPool = logging.getLogger('logTxPool')
    dictionary = web3.geth.txpool.status()
    logTxPool.info(dictionary["pending"])
    
    try:
        web3.eth.waitForTransactionReceipt(tx_hash, timeout=600)
        elapsed = time.perf_counter() - startTime
        
        receipt = web3.eth.getTransactionReceipt(tx_hash)
        gas = receipt["gasUsed"]
        price = web3.eth.gasPrice
        cost = gas*price
        costEther = cost/1000000000000000000
    except:
        elapsed = 0

    logTxTime = logging.getLogger('logTxTime')
    logTxTime.info(elapsed)

    logTxCost = logging.getLogger('logTxCost')
    logTxCost.info(costEther)

def gerarEnderecos():
    global web3
    global enderecos

    print('\nGerando/Carregando Endereços')
    ends = ""
    
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
    tx_hash = contrato.functions.addUsuario(valid_address).transact()
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)

def rastrearProduto():
    print('--- Rastreio de Produto ---')
    #code = input('Código do Produto: ')

# -- MAIN -- #

for param in sys.argv :
    SUPPLY_CHAIN = str(param)

res = conectarContrato()
if(res == "Conectado ao contrato!"):
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
from web3 import Web3
from web3.contract import ConciseContract
import json
import binascii



provider = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(provider))

ABI = json.loads('''[
  {
    "constant": false,
    "inputs": [
      {
        "name": "_to",
        "type": "address"
      },
      {
        "name": "_amount",
        "type": "uint256"
      },
      {
        "name": "_from",
        "type": "address"
      }
    ],
    "name": "transaction",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_from",
        "type": "address"
      }
    ],
    "name": "getSolde",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_to",
        "type": "address"
      },
      {
        "name": "_amount",
        "type": "uint256"
      }
    ],
    "name": "addSolde",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": true,
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "_from",
        "type": "address"
      },
      {
        "indexed": true,
        "name": "_to",
        "type": "address"
      },
      {
        "indexed": true,
        "name": "_amount",
        "type": "uint256"
      }
    ],
    "name": "Transfert",
    "type": "event"
  }
]''')

ADDRESS = '0x3f85D0b6119B38b7E6B119F7550290fec4BE0e3c'
contract_instance = web3.eth.contract(abi=ABI, address=ADDRESS, ContractFactoryClass=ConciseContract)
addr = "0x8fA91A9043C8c506BBaa419648dD28c4C8140643"
#tx = contract_instance.addSolde(add, 55555, transact={'from': web3.eth.accounts[0], 'gasPrice': 20000})
#print(web3.eth.accounts[0])
#tx1 = contract_instance.transaction(web3.eth.accounts[1] ,11,web3.eth.accounts[0],transact={'from': web3.eth.accounts[0]})
#print(binascii.hexlify(bytearray(tx)))
print(contract_instance.getSolde(addr))





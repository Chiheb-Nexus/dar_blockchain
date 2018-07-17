import json
from web3 import Web3
from solc import compile_source
import time
from Generate_wallet import Wallet
from ethereum.transactions import Transaction
import rlp

class DeployContract:
	contract_interface = ''
	GAS = 41000
	web3 = ''
	infura_provider = 'https://ropsten.infura.io/FPWVtgMMHZZZtbLvkwdy'
	def __init__(self, file_name='balance.sol', contract_name='FixedSupplyToken'):
		data = ''
		self.web3 = Web3(Web3.HTTPProvider(self.infura_provider))
		with open(file_name, 'r') as f:
			data = f.read()

		compiled_data = compile_source(data)
		self.contract_interface = compiled_data.get('<stdin>:FixedSupplyToken')

	def deploy(self,_from,private_key):
		if self.contract_interface:
			infura_node = self.web3
			nonce =   self.web3.eth.getTransactionCount(_from)
			gas_price = self.web3.eth.gasPrice
			transaction = {
				'from': _from,
				'gas': 2000000,
				'gasPrice':gas_price,
				'nonce': nonce,
				'chainId': self.web3.net.version
			}
			signed = self.web3.eth.account.signTransaction(transaction,private_key)
			contract = self.web3.eth.contract(abi=contract_interface.get('abi'), bytecode=contract_interface.get('bin'))
			print('Contract created')			
			tx.sign(private_key)
			raw_tx = rlp.encode(tx)
			raw_tx_hex = web3.toHex(raw_tx)
			tx_hash = web3.eth.sendTransaction(raw_tx_hex)
			#tx_hash = contract.deploy()
			while infura_node.eth.getTransactionReceipt(tx_hash) is None:
				print('Waiting confirmation ...')
				time.sleep(1)

			tx_receipt = infura_node.eth.getTransactionReceipt(tx_hash)
			contract_address = tx_receipt.get('contractAddress')

			with open('contract_informations.json', 'w') as f:
				f.write(json.dumps({
					'abi': self.contract_interface.get('abi'),
					'contract_address': contract_address
					}))

			print('Done!')
		else:
			raise Exception('Contract interface in null')


if __name__ == '__main__':
	a = DeployContract()
	a.deploy(_from = '0x88CB10Cc719f5a45f28057e7E51f936a04A9B9C0', private_key = '826f7648aa9bbad5d8307e51e45304fe4b0c83aae41d9661c454d02366357f5b')


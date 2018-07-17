from web3 import Web3
from web3.contract import ConciseContract
from solc import compile_source
import json
import time

class InfuraNode:
	infura_provider = 'https://ropsten.infura.io/FPWVtgMMHZZZtbLvkwdy'

	def __init__(self):
		self.w3 = Web3(Web3.HTTPProvider(self.infura_provider))


class PersonalNode:
	personal_provider = 'http://159.65.243.41:8545'

	def __init__(self):
		self.w3 = Web3(Web3.HTTPProvider(self.personal_provider))


class DeployContract:
	contract_interface = ''
	GAS = 41000
	def __init__(self, file_name='test.sol', contract_name='Balance'):
		data = ''
		with open(file_name, 'r') as f:
			data = f.read()

		compiled_data = compile_source(data)
		self.contract_interface = compiled_data.get('<stdin>:Balance')

	def deploy(self):
		if self.contract_interface:
			personal_node = PersonalNode().w3
			infura_node = InfuraNode().w3
			contract = personal_node.eth.contract(abi=self.contract_interface.get('abi'), bytecode=self.contract_interface.get('bin'))
			tx_hash = contract.deploy(transaction={'from': personal_node.eth.accounts[0], 'gas': self.GAS})
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
	a.deploy()

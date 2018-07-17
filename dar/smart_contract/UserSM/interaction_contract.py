from web3 import Web3
from web3.contract import ConciseContract
from ethereum import utils
import os
from django.conf import settings
#import settings


class InteractionContract:
	def __init__(self):
		provider = 'https://ropsten.infura.io/FPWVtgMMHZZZtbLvkwdy'
		ABI = settings.ABI
		CONTRACT_ADDRESS = settings.CONTRACT_ADDRESS
		try:
			self.w3 = Web3(Web3.HTTPProvider(provider))
			self.contract_instance = self.w3.eth.contract(abi=ABI, address=CONTRACT_ADDRESS)
			self.contract_instance_consice = self.w3.eth.contract(abi=ABI, address=CONTRACT_ADDRESS, ContractFactoryClass=ConciseContract)
		except Exception as e:
			print('Exception at InteractionContract',e)

	def generate_wallet(self):
		''' '''
		try:
			private_key = self.w3.toHex(utils.sha3(os.urandom(4096)))
			public_key  = utils.checksum_encode(utils.privtoaddr(private_key))
			return private_key, public_key
		except Exception as e:
			raise Exception('Error while generating a wallet: ', e)


	def transfer(self, from_privkey=None, from_pubkey=None, to_pubkey=None, value=0):
		''' ADD SOLDE '''

		if not from_privkey or not from_pubkey or not to_pubkey:
			raise Exception('Verify transfer arguments!')

		instance_tx = self.contract_instance.functions.addSolde(to_pubkey, value).buildTransaction({
			'chainId': self.w3.net.version,
			'gasPrice': self.w3.eth.gasPrice,
			'nonce': self.w3.eth.getTransactionCount(from_pubkey),
			})
		signed_tx = self.w3.eth.account.signTransaction(instance_tx, from_privkey)
		tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
		return self.w3.toHex(tx_hash)

	def total_supply(self):
		return self.contract_instance_consice.totalSupply()

	def balance_of(self, address=None):
		if not address:
			raise Exception('Address not valid')
		return self.contract_instance_consice.balanceOf(address)

	def transfer_from(self, from_privkey=None, from_pubkey=None, to_pubkey=None, value=0):
		if not from_pubkey or not from_privkey or not to_pubkey:
			raise Exception('From or To addresses are not valid')

		instance_tx = self.contract_instance.functions.transferFrom(from_pubkey, to_pubkey, value).buildTransaction({
			'chainId': self.w3.net.version,
			'gasPrice': self.w3.eth.gasPrice,
			'nonce': self.w3.eth.getTransactionCount(settings.PUBKEY_DEFAULT_ACCOUNT),
			'gas': self.w3.eth.estimateGas({'from':settings.PUBKEY_DEFAULT_ACCOUNT}),
		})
		signed_tx = self.w3.eth.account.signTransaction(instance_tx, settings.PRIVKEY_DEFAULT_ACCOUNT)
		try:
			tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
		except Exception as e:
			print('echec transaction in interaction contract l:68',e)
			return None
		
		return self.w3.toHex(tx_hash)


if __name__ == '__main__':
	ADDRESSE1 = '0x88CB10Cc719f5a45f28057e7E51f936a04A9B9C0'
	PRIVATEKEY1 = '826f7648aa9bbad5d8307e51e45304fe4b0c83aae41d9661c454d02366357f5b'
	ADDRESSE2 = '0xeE362b4A7EEAfC151eaF3E68Ff3297Db76ff5AC5'
	a = InteractionContract()
	#b = a.transfer(from_privkey=PRIVATEKEY1, from_pubkey=ADDRESSE1, to_pubkey='0x9e1cdef1557b1b61b54247b89c5a1599521aa51fd4c0aa5386675d65ccbd9ab7', value=1122)
	#print(b)
	#print(a.total_supply())
	#print(a.balance_of(ADDRESSE2))
	#print(a.transfer_from(from_privkey='0x073a655678bb6f7d314dfe3a8a50858a2716e0527800f104851242560a1a14e8', 
	#	from_pubkey='0x8079f2c956fEB52cd156Bf88Ffd4CCdE17c612D4', to_pubkey='0x88CB10Cc719f5a45f28057e7E51f936a04A9B9C0', value=1000))
	#print(a.generate_wallet())
	print(a.transfer(from_privkey='826f7648aa9bbad5d8307e51e45304fe4b0c83aae41d9661c454d02366357f5b',
					from_pubkey='0x88CB10Cc719f5a45f28057e7E51f936a04A9B9C0',
					to_pubkey='0xeE362b4A7EEAfC151eaF3E68Ff3297Db76ff5AC5',value=100))



#
# Dar Blockchain
#
# © Dar Blockchain:
#

import os
from web3 import Web3
from web3.contract import ConciseContract
from ethereum import utils
from django.conf import settings

__authors__ = ['Chiheb Nexus', 'Mounir Ben Romdhane']

class InteractionContract:
	'''
	Wrapper qui permet l'interaction avec les smart contracts de type ERC20
	Wrapper qui permet l'interaction avec le smart contract de dar blockchain
	'''
	def __init__(self):
		'''
		Initialiser la classe d'interaction avec le Smart Contract
		@param: w3: Instance de Web3 avec son Provider
		@param: contract_instance: Instance du contrat
		@param: contract_instance_consice: Instance du contrat en mode ConciseContract
		'''

		self.w3 = Web3(Web3.HTTPProvider(settings.PROVIDER))
		self.contract_instance = self.w3.eth.contract(
											abi=settings.ABI, 
											address=settings.CONTRACT_ADDRESS)
		self.contract_instance_consice = self.w3.eth.contract(
											abi=settings.ABI, 
											address=settings.CONTRACT_ADDRESS, 
											ContractFactoryClass=ConciseContract)

	def transfer(self, from_privkey=settings.PRIVKEY_DEFAULT_ACCOUNT, 
					from_pubkey=settings.PUBKEY_DEFAULT_ACCOUNT, to_pubkey=None, value=0):
		'''
		Ajouter solde à un client de Dar
		@param: fom_privkey: Clé privée du Owner du Smart Contract
		@param: from_pubkey: Clé publique du Owner du Smart Contract
		@param: to_pubkey: Clé publique du client de Dar
		@param: value: Token dar à transférer du Smart Contract vers le client du Dar
		'''
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
		'''
		Retourner le totalSupply du Smart Contract Dar
		'''
		return self.contract_instance_consice.totalSupply()

	def balance_of(self, address=None):
		'''
		Retourner la balancce de l'adresse
		@param: address : L'adresse qu'on cherche à connaitre sa balance en token Dar
		'''
		if not address:
			raise Exception('Address not valid')
		return self.contract_instance_consice.balanceOf(address)

	def transfer_from(self, from_privkey=settings.PRIVKEY_DEFAULT_ACCOUNT, 
						from_pubkey=settings.PUBKEY_DEFAULT_ACCOUNT, to_pubkey=None, value=0):
		'''
		Transférer des tokens Dar d'une adresse à une autre (d'un client du Dar à un autre)
		@param: from_pubkey: L'adresse publique de celui qui va envoyer des tokens
		@param: from_privkey: La clé privée de celui qui va envoyer des tokens
		@param: to_pubkey: L'adresse publique de ccelui qui va envoyer des tokens
		@value: Le montant en token Dar
		'''
		if not from_pubkey or not from_privkey or not to_pubkey:
			raise Exception('From or To addresses are not valid')

		instance_tx = self.contract_instance.functions.transferFrom(from_pubkey, to_pubkey, value).buildTransaction({
			'chainId': self.w3.net.version,
			'gasPrice': self.w3.eth.gasPrice,
			'nonce': self.w3.eth.getTransactionCount(settings.PUBKEY_DEFAULT_ACCOUNT),
			'gas': self.w3.eth.estimateGas({'from': settings.PUBKEY_DEFAULT_ACCOUNT}),
		})
		signed_tx = self.w3.eth.account.signTransaction(instance_tx, settings.PRIVKEY_DEFAULT_ACCOUNT)
		tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
		return self.w3.toHex(tx_hash)


# Test
if __name__ == '__main__':
	ADDRESSE1 = '0x88CB10Cc719f5a45f28057e7E51f936a04A9B9C0'
	PRIVATEKEY1 = '826f7648aa9bbad5d8307e51e45304fe4b0c83aae41d9661c454d02366357f5b'
	ADDRESSE2 = '0xeE362b4A7EEAfC151eaF3E68Ff3297Db76ff5AC5'
	a = InteractionContract()
	#b = a.transfer(from_privkey=PRIVATEKEY1, from_pubkey=ADDRESSE1, to_pubkey='0x9e1cdef1557b1b61b54247b89c5a1599521aa51fd4c0aa5386675d65ccbd9ab7', value=1122)
	#print(b)
	#print(a.total_supply())
	print(a.balance_of(ADDRESSE2))
	#print(a.transfer_from(from_privkey='0x073a655678bb6f7d314dfe3a8a50858a2716e0527800f104851242560a1a14e8', 
	#	from_pubkey='0x8079f2c956fEB52cd156Bf88Ffd4CCdE17c612D4', to_pubkey='0x88CB10Cc719f5a45f28057e7E51f936a04A9B9C0', value=1000))
	#print(a.generate_wallet())

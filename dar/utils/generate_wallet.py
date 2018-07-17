#
# Générer des clés privées et publique valides pour la blockchain d'Ethereum
#
#

from ethereum import utils
from web3 import Web3
from django.conf import settings
import os

__authors__ = ['Chiheb Nexus', 'Mounir Ben Romdhane']

class GenerateWallet:
	def __init__(self):
		provider = settings.PROVIDER
		self.web3 = Web3(Web3.HTTPProvider(provider))

	def generate_wallet(self):
		try:
			private_key = self.web3.toHex(utils.sha3(os.urandom(4096)))
			public_key  = utils.checksum_encode(utils.privtoaddr(private_key))
			return private_key, public_key
		except Exception as e:
			raise Exception('Error while generating a wallet: ', e)


# Test
if __name__ == '__main__':
	a = GenerateWallet()
	print(a.generate_wallet())

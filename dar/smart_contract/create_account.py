from web3 import Web3
from web3.contract import ConciseContract
import json
import binascii
from dar.models import *



class Account():
	provider = "http://127.0.0.1:8545"
	def __init__(self):
		self.web3 = Web3(Web3.HTTPProvider(self.provider))

	def create_account(self, passphrase):
		r#eturn self.web3.personal.newAccount(passphrase)


	def add_solde(self,solde,user):
		''' add solde to BD '''
		''' add solde to smart-contract '''
		#User_BD().add_solde(user=user,solde=solde)
		#print(UserSM().add_solde(user=user,solde=solde))
		print('add solde create_account')


if __name__ == '__main__':
	print ( Account().create_account('hello'))







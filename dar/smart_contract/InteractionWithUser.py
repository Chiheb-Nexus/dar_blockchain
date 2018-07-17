from .aes import AESCipher
from django.conf import settings
from .UserSM.interaction_contract import InteractionContract

from django.contrib.auth.models import User
import django.db.utils as djExceptions
from ..models import DarUser,Dyar
from validate_email import validate_email
from django.conf import settings


class InteractionWithUser():

	def __init__(self):
		try:
			self.contract = InteractionContract()
		except Exception as e:
			print(e)
			raise Exception('Error while instantiate InteractionContract')

	def add_solde(self,value=0,user=None):

		if not user:
			raise Exception("value missed class user")
		try:

			tx = self.contract.transfer_from(from_privkey=settings.PRIVKEY_DEFAULT_ACCOUNT,from_pubkey=settings.PUBKEY_DEFAULT_ACCOUNT,
				to_pubkey=user.public_address,value=value)
			print("test2")

			user.solde += value
			user.save()
		except Exception as e:
			print(e)
			raise Exception('error while adding solde')
		return tx
		

	def get_solde(self,user=None):

		if not user:
			raise Exception("value missed class user")

		try:
			solde_sm = self.contract.balance_of(address = user.public_address)
		except Exception as e:
			print(e)
			raise Exception("get solde failed",e)
		#from DATABASES		
		solde_db = user.solde
		return solde_sm,solde_db

	def transfer(self,user_to= None, user_from = None,value=0):

		if not user_from:
			raise Exception("value user_to missed ")
		if not user_to:
			pub_key_to = settings.PUBKEY_DEFAULT_ACCOUNT
		else:
			pub_key_to = user_to.public_address

		print("user solde from db	:",user_from.solde)
		print("value				:",value)
		if user_from.solde < value:
			raise Exception ("value to transfer inferior")

		decrypt = AESCipher(key = user_from.tel)

		try:

			tx = self.contract.transfer_from(from_privkey=decrypt.decrypt(enc=user_from.private_key), from_pubkey=user_from.public_address,
										 to_pubkey=pub_key_to, value=value)	
		except Exception as e:
			print('in interaction with user L:74     ',e)
			return None
			raise Exception("transaction failed", e)
		print('user solde ',user_from.solde)
		user_from.solde -= value
		user_from.save()
		return tx












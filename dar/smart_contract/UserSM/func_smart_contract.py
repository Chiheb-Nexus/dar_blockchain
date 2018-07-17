from generate_wallet import Wallet
from web3.contract import ConciseContract

class Func_smart_contract:

	ADDRESSE1 = '0x88CB10Cc719f5a45f28057e7E51f936a04A9B9C0'
	PRIVATEKEY1 = '826f7648aa9bbad5d8307e51e45304fe4b0c83aae41d9661c454d02366357f5b'

	ADDRESSE2 = '0xeE362b4A7EEAfC151eaF3E68Ff3297Db76ff5AC5'
	PRIVATEKEY2 = 'b67ab8e3c04f73f0fcad6082e53a498f04b11de7bd067c81dc28652b8975931c'
	
	def __init__(self):
		self.wallet = Wallet()
		self.web3 = self.wallet.web3


	def transfer(self, private_key ,value, _to, _from):
		'''ADD SOLDE '''
		try:
			c = self.wallet.transaction_contract(private_key=private_key,_to= _to, _from=_from)
			unicorns = self.web3.eth.contract(abi=c['abi'], address=c['contract_address'])
			nonce = self.web3.eth.getTransactionCount(c['_from'])

			unicorn_tx = unicorns.functions.addSolde(_to, value).buildTransaction({
				'chainId': self.web3.net.version,
				'gas': self.web3.eth.estimateGas({'to': _to, 'data': '0x0', 'from': _from}),
				'gasPrice': self.web3.eth.gasPrice,

				'nonce': nonce,
				})

			print('unicorn', unicorn_tx)

			data = unicorn_tx.get('data') if unicorn_tx.get('data') else '0x00'
			unicorn_tx['gas'] = self.web3.eth.estimateGas({'to': _to, 'data': data})
			#unicorn_tx['gas'] = 36272
			#unicorn_tx['data'] = b'0xe43efe0e00000000000000000000000088cb10cc719f5a45f28057e7e51f936a04a9b9c0000000000000000000000000000000000000000000000000000000000000000b'
			print(unicorn_tx)
			signed_txn = self.web3.eth.account.signTransaction(unicorn_tx, private_key=c['private_key'])
			print(signed_txn)
			tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
			print('raw: ', self.web3.toHex(signed_txn.rawTransaction))

			#return self.web3.toHex(tx_hash)

		except Exception as e:
			raise Exception('Transaction failed: ', e)

	def transfer_from(self,_from,_to,value,private_key):
		''' TRANSACTION FROM => TO  '''
		pass

	def balance_of(self,addresse):
		''' GET SOLDE'''
		try:
			c = self.wallet.transaction_contract(_to= addresse, _from=addresse)
			contract_instance =	self.web3.eth.contract(abi=c['abi'], address=c['contract_address'], ContractFactoryClass=ConciseContract)
			return contract_instance.balanceOf(addresse)			
		except Exception as e:
			raise Exception('Transaction failed: ', e)		


if __name__ == '__main__':

	a = Func_smart_contract()
	#b= a.transfer(value= 110, _to= a.ADDRESSE1, private_key = a.PRIVATEKEY1, _from=a.ADDRESSE1)
	address_owner = "0x88CB10Cc719f5a45f28057e7E51f936a04A9B9C0"
	c= a.balance_of(addresse=address_owner)
	print(b)
	print(c)



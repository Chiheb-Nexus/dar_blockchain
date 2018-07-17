#
# Dar Blockchain
#
# © Dar Blockchain:
#

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.apps import apps
import uuid

__authors__ = ['Chiheb Nexus', 'Mounir Ben Romdhane']

# Importer les models: DarUser et Dyar
DarUser = apps.get_model('dar', 'darUser')
Dyar = apps.get_model('dar', 'dyar')

class RegisterUser:
	'''
	Enregistrer l'utilisateur et darUser
	'''
	def __init__(self, **kwargs):
		'''
		Initialiser les données de RegisterUser
		@params: email: Email de l'utilisateur -> Il doit etre valide
		@params: dar: UUID du dar doit etre valide
		@params: username: L'username de l'utilisateur à enregistrer
		@params: telephone: Le téléphone de l'utilisateur à enregistrer (doit etre valide)
		@params: password: Le mot de passe de l'utilisateur (doit etre un mot de passe valide)
		'''
		elems = ['username', 'telephone', 'email', 'password', 'dar']
		if not kwargs or not all(k in kwargs for k in elems):
			raise Exception('''RegisterUser arguments must be valid and not null!
				Arguments: "{0}"'''.format(', ').join(elems))
		try:
			validate_email(kwargs.get('email'))
		except ValidationError:
			raise Exception('{0} is not a valid email'.format(kwargs.get('email')))
		else:
			self.email = kwargs.get('email')

		try:
			self.dar = kwargs.get('dar')
		except ValueError as e:
			raise Exception('Not valid UUID')


		self.username = kwargs.get('username')
		self.telephone = kwargs.get('telephone')
		self.password = kwargs.get('password')

	def register(self, solde=0):
		'''
		Enregistrer DarUser
		Étapes: Création de l'utilisateur -> trouver l'instance du Dar -> Création de DarUser
		'''
		try:
			client = User.objects.create_user(username=self.username, password=self.password, email=self.email)
			client.is_active = False
			client.save()
		except IntegrityError as e:
			raise Exception('User: {0} already Exist!'.format(self.username))

		try:
			dar = Dyar.objects.get(_uuid=self.dar)
		except IntegrityError as e:
			raise Exception('Cannot find DAR')

		try:
			dar_user = DarUser.objects.create(tel=self.telephone, solde=solde, dar=dar, user=client)
		except IntegrityError as e:
			raise Exception('Cannot create DAR user')

		return dar_user







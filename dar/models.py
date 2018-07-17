#
# Dar Blockchain
#
# © Dar Blockchain:
#

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from uuid import uuid4
from dar.utils.generate_wallet import GenerateWallet
from dar.utils.aes import AESCipher

__authors__ = ['Chiheb Nexus', 'Mounir Ben Romdhane']


class Dyar(models.Model):
	'''
	Les champs requis pour un coworking space de Dar Blockchain
	@param: nom: Nom du DAR
	@param: adresse: Adresse du DAR
	@param: Pack: Un pack peut etre affecté à plusieurs dyars

	@FIXME: Autres champs ?
	'''
	_uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
	nom = models.CharField(verbose_name=_('Nom dar'), max_length=50)
	address = models.CharField(verbose_name=_('Adresse dar'), max_length=100)

	def __str__(self):
		return '{0} - {1}'.format(self.nom, self.address)

class Pack(models.Model):
	'''
	Les packs offerts par Dar Blockchain
	@param: titre: Titre du pack
	@param: informations: Des informations supplémentaires au pack offert
	'''
	_uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
	titre = models.CharField(verbose_name=_('titre'), blank=False, max_length=50)
	informations = models.TextField(verbose_name=_('informations'), max_length=200, blank=False)
	price = models.FloatField(verbose_name=_('Prix Abonnement'), default=0.0)
	dar = models.ForeignKey(
		Dyar,
		verbose_name=_('Dar'), 
		on_delete=models.DO_NOTHING, 
		blank=True, 
		null=True,
		related_name='dp'
	)

	def __str__(self):
		return '{0} - {1} - {2}'.format(
			self.dar,
			self.titre, 
			self.price,
		)


class DarUser(models.Model):
	'''
	Les champs requis pour un utilisateur de Dar Blockchain
	@param: user: OneToOneField avec le model User par défaut que propose Django
	@param: tel: Numéro de téléphone de l'utilisateur de Dar Blockchain
	@param: solde: Solde de l'utilisateur de Dar Blockchain -> Synchronisation avec son solde en token sur le Smart Contract
	@param: is_client: L'utilisateur de Dar Blockchain est t-il un client ou vendeur ?
	@param: is_abonn: L'utiliateur de Dar Blockchain est t-il un abonné ?
	@param: public_address: L'adresse publique de l'utilisateur de Dar Blockchain
	@param: private_key: La clé privée de l'utilisateur de Dar Blockchain
	'''
	_uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	tel = models.CharField(
		validators=[
			RegexValidator(regex=r'^\+\d{11}$', message=_('Wrong Phone Number'))
		], max_length=12,
		verbose_name=_('N° Téléphone')
	)
	solde = models.FloatField(verbose_name=_('Solde'), default=0)
	is_client = models.BooleanField(verbose_name=_('Is Client'), default=False)
	is_abonn = models.BooleanField(verbose_name=_('Is Abonne'), default=False)
	is_admin = models.BooleanField(verbose_name=_('Is Admin'), default=False)
	dar = models.ForeignKey(
		Dyar, 
		verbose_name=_('Dar Du User'), 
		on_delete=models.DO_NOTHING,
		related_name='dar'
	)
	public_address = models.CharField(
		verbose_name=_('Public Address'),
		max_length= 200, 
		blank=True, 
		null=True
	)
	private_key= models.CharField(
		verbose_name=_('Private Key'),
		max_length= 200, 
		blank=True, 
		null=True
	)
	is_saved = models.BooleanField(verbose_name=_('Is saved'), default=False, blank=False, null=False)

	@staticmethod
	def pre_save(sender, instance, **kwargs):
		'''
		Générer un pair de clé publique et privée
		'''

		if not instance.is_saved:
			privkey,pubkey = GenerateWallet().generate_wallet()
			cipher = AESCipher(key=instance.tel)
			instance.private_key = cipher.encrypt(privkey)
			instance.public_address = pubkey
			instance.is_saved = True

	def __str__(self):
		return '{0} - {1}'.format(self.user.username, self.solde)

pre_save.connect(DarUser.pre_save, DarUser)


class Abonnement(models.Model):
	'''
	Les abonnements avec Dar Blockchain
	@param: pack: Un ForeignKey avec Pask -> Relation Many to One
	@param: user_abonne: L'utilisateur abonné au pack -> Relation Mnay to One
	@param: date_debut: Date du début de l'abonnement
	@param: date_fin: Date de la fin de l'abonnement
	@param: is_group: L'abonnement contient t-il un groupe de personnes ?
	'''
	_uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
	pack = models.ForeignKey(
		Pack, 
		verbose_name=_('Pack'), 
		blank=False, 
		null=False, 
		on_delete=models.DO_NOTHING,
		related_name='ap'
	)
	user_abonne = models.ForeignKey(
		DarUser, 
		verbose_name=_("Abonne"),
		blank=False, 
		on_delete=models.DO_NOTHING
	)
	date_debut = models.DateTimeField(verbose_name=_('Date Debut'), blank=False)
	date_fin = models.DateTimeField(verbose_name=_('Date Fin'), blank=False)
	is_group = models.BooleanField(verbose_name=_('is for group'), default=False)

	def __str__(self):
		return '{0} - {1} - {2}'.format(
			self.pack, 
			self.date_debut, 
			self.date_fin 
		)

	def calculate_price(self, date_debut, date_fin):
		'''
		Méthode pour calculer le prix de l'abonnement selon le pack choisi
		@FIXME: Compléter le calcul du prix selon le pack choisi
		'''
		# logique autour de self.price
		return self.price


class Fonction(models.Model):
	'''
	Fonction de la salle
	@param: fonction_name: Titre de la fonction d'une salle
	'''
	_uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
	fonction_name = models.CharField(verbose_name=_('nom fonction salle'), blank=False, max_length=50)
	description = models.TextField(verbose_name=_('Description de la fonction'))

	def __str__(self):
		return '{0}'.format(self.fonction_name)


class Salle(models.Model):
	'''
	Salle: Professionnelle et non professionnelle
	@pram: user: Un ForeignKey avec DarUser -> Relation Many to One
	@param: identifiant: Identifiant de l'utilisateur
	@param: fonction_salle : ForeignKey avec Fonction -> Salle a plusieurs fonctions -> Relation Many to One
	@param: capacity: Capacité d'une salle Professionnelle
	@param: nb_chaise: Nombre de chaises par salle
	@param: superficie: La superficie d'une salle professionnelle
	@pram: price: Prix de location d'une salle professionnelle
	@param: dar: La salle professionnelle appartient à quelle Dar
	@param: salle_prof: Booléen: La salle est professionnelle ou non
	'''
	_uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
	user = models.ForeignKey(
		DarUser, 
		verbose_name=_('User'), 
		blank=False,
		null=True, 
		related_name="us", 
		on_delete=models.DO_NOTHING
	)
	nom_salle = models.CharField(blank=False, verbose_name=_('ID'), max_length=50)
	fonction_salle = models.ForeignKey(
		Fonction, 
		verbose_name=_('Fonction'), 
		blank=False, 
		on_delete=models.DO_NOTHING,
		related_name='snom'
	)
	capacity = models.IntegerField(verbose_name=_('capacite salle'), blank=False)
	nb_chaise = models.IntegerField(verbose_name=_('nombre de chaise'), blank=False)
	superficie = models.FloatField(verbose_name=_('superficie'), blank=False)
	price = models.FloatField(verbose_name=_('Prix Salle Prof'))
	salle_prof = models.BooleanField(verbose_name=_('Salle Professionnelle'), default=False)
	dar = models.ForeignKey(
		Dyar, 
		verbose_name=_('dar'), 
		blank=False,
		related_name="spd", 
		on_delete = models.DO_NOTHING
	)

	def __str__(self):
		is_salle_prof = 'Salle Prof' if self.salle_prof else 'Salle Non Professionnelle'
		return '{0} - {1} - {2} - {3}'.format(
			self.nom_salle, 
			self.dar.nom, 
			self.price, 
			is_salle_prof
		)


class Panier(models.Model):
	'''
	Les transactions d'une Salle Non Professionnelle
	@param: salle: Une relation One to One avec SalleNonProf
	@param: user: User qui a fait la transaction
	@param: montant: Montant de la transaction
	@param: date: La date de la transaction
	@tx_hash: Transaction Hash du panier validé -> retrouvé avec web3
	'''

	_uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
	dar = models.ForeignKey(
		Dyar, 
		on_delete=models.DO_NOTHING, 
		verbose_name=_('Dar'), 
		related_name='padar'
	)
	user = models.ForeignKey(
		DarUser, 
		verbose_name=_('User'), 
		on_delete=models.DO_NOTHING, 
		related_name='pauser'
	)
	montant = models.FloatField(verbose_name=_('Montant'), blank=True)
	date = models.DateTimeField(auto_now_add=True, blank=True)
	tx_hash = models.CharField(verbose_name=_('tx hash'),blank=False,max_length=120)

	def __str__(self):
		return '{0} - {1}'.format(self.user, self.montant)


class Produit(models.Model):
	'''
	Les produits offerts par Dar Blockchain
	@param: nom: Nom du produit
	@param: description: Description du produit
	@param: quantity: Quantité du produit
	@param: price: Prix du produit
	@salle: Les produits sont affectés aux salles: ForeignKey avec SalleNonProf: Many to One
	'''

	_uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
	nom = models.CharField(verbose_name=_('Nom Produit'), blank=False, max_length=50)
	description = models.TextField(verbose_name=_('Description'), blank=False, max_length=200)

	def __str__(self):
		return '{0}'.format(self.nom)

class AlimentationProduit(models.Model):
	_uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
	dar = models.ForeignKey(
		Dyar,
		verbose_name=_('Dar'),
		blank=False,
		null=True,
		on_delete=models.DO_NOTHING,
		related_name='ald'
	)
	produit = models.ForeignKey(
		Produit,
		verbose_name=_('Produit'),
		blank=False,
		null=False,
		on_delete=models.DO_NOTHING,
		related_name='alpd'
	)
	quantity = models.IntegerField(verbose_name=_('Quantité'), default=0)
	prix = models.FloatField(verbose_name=_('Prix'), default=0.0)
	date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date'))

	def __str__(self):
		return '{} - {} - {} - {}'.format(
			self.dar, 
			self.produit,
			self.quantity,
			self.prix
		)

class ProduitSalle(models.Model):
	_uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
	salle = models.ForeignKey(
		Salle,
		verbose_name=_('Salle'),
		blank=False,
		null=False,
		on_delete=models.DO_NOTHING,
		related_name='prs'
	)
	alimentation_produit = models.ForeignKey(
		AlimentationProduit,
		verbose_name=_('Alimentaion Produit'),
		blank=False,
		null=False,
		on_delete=models.DO_NOTHING,
		related_name='prp'
	)

	quantity = models.IntegerField(verbose_name=_('Quantité'), default=0)
	price = models.FloatField(verbose_name=_('Prix'), default=0.0)
	date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date'))



class Transaction(models.Model):
	'''
	Les transactions des utilisateurs
	@param: produit: Produit acheté: ForeignKey avec Produit -> Many To One
	@param: quantity: Quantité des produits achetés
	@param: Panier: Panier avec lequel la transaction est affecté: ForeignKey avec Panier

	'''
	_uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
	produit = models.ForeignKey(
		ProduitSalle, 
		verbose_name=_('Produit'), 
		blank=True, 
		null=True, 
		related_name='txprod', 
		on_delete=models.DO_NOTHING
	)
	quantity = models.IntegerField(verbose_name=_('Quantité'), default=0)
	panier = models.ForeignKey(
		Panier, 
		verbose_name=_('Panier'), 
		blank=False, 
		null=False, 
		related_name= 'txpan', 
		on_delete=models.DO_NOTHING
	)

	def __str__(self):
		return '{0} - {1} - {2}'.format(
			self.produit, 
			self.quantity, 
			self.panier
		)


class Reservation(models.Model):
	'''
	Réservation des Salles Professionnelles
	@param: salle: Salle réservée
	@param: date_debut: Date de début de la réservation
	@param: date_fin: Date de fin d'une réservation
	@param: client: Un ForeignKey avec DarUser -> Client qui a réservé la salle -> Relation Many to One
	'''
	_uuid = models.UUIDField(unique=True, default= uuid4, editable=False)
	salle = models.ForeignKey(
		Salle, 
		verbose_name=_('Salle'), 
		blank=True, 
		on_delete=models.DO_NOTHING, 
		related_name='sres'
	)

	date_debut = models.DateTimeField(verbose_name=_('Date Debut'), blank=False)
	date_fin = models.DateTimeField(verbose_name=_('Date Fin'), blank=False)
	client = models.ForeignKey(
		DarUser, 
		verbose_name=_('Client'), 
		related_name='res', 
		on_delete=models.DO_NOTHING
	)
	panier = models.ForeignKey(
		Panier, 
		verbose_name=_('Panier'), 
		blank=False, 
		null=False, 
		related_name= 'respan', 
		on_delete=models.DO_NOTHING
	)

	def __str__(self):

		return '{0}'.format(self.panier)

class TransactionReservation(models.Model):
	'''
	'''
	_uuid = models.UUIDField(unique=True,default = uuid4 , editable=False)
	user = models.ForeignKey(
		DarUser,
		verbose_name=_('User'),
		blank=False,
		null=False,
		related_name='txr',
		on_delete=models.DO_NOTHING
	)
	salle = models.ForeignKey(
		Salle,
		verbose_name=_('Salle'),
		blank=False,
		null=False,
		related_name='trs',
		on_delete=models.DO_NOTHING
	)
	date_debut = models.DateTimeField(verbose_name=_('Date Début'))
	date_fin = models.DateTimeField(verbose_name=_('Date Fin'))
	panier = models.ForeignKey(
		Panier,
		verbose_name=_('Panier'),
		blank=False,
		null=False,
		related_name='trp',
		on_delete=models.DO_NOTHING
	)

	def __str__(self):
		return self.panier
	
class Formation(models.Model):
	'''
	'''
	_uuid = models.UUIDField(unique=True,default = uuid4 , editable=False)
	titre = models.CharField(verbose_name=_('Titre'), max_length=200)
	description = models.TextField(verbose_name=_('Description'))

	def __str__(self):
		return self.titre

class FormationDar(models.Model):
	'''
	'''
	_uuid = models.UUIDField(unique=True,default = uuid4 , editable=False)
	formateur = models.ForeignKey(
		DarUser,
		verbose_name= _('Formateur'),
		blank=False,
		null=False,
		related_name='fdar',
		on_delete=models.DO_NOTHING
	)
	formation = models.ForeignKey(
		Formation,
		verbose_name=_('Formation'),
		blank=False,
		null=False,
		related_name='fordar',
		on_delete=models.DO_NOTHING
	)
	salle = models.ForeignKey(
		Salle,
		verbose_name=_('Salle'),
		blank=False,
		null=False,
		related_name='fs',
		on_delete=models.DO_NOTHING
	)
	date_debut = models.DateTimeField(verbose_name=_('Date Debut'))
	date_fin = models.DateTimeField(verbose_name=_('Date Fin'))
	price = models.FloatField(verbose_name=_('Prix'), default=0.0)
	nb_place = models.IntegerField(verbose_name=_('Nombre de place'), default=0)
	place_restant = models.IntegerField(verbose_name=_('place restant'),default=0)



class TransactionFormation(models.Model):
	'''
	'''
	_uuid = models.UUIDField(unique=True,default = uuid4 , editable=False)
	user = models.ForeignKey(
		DarUser,
		verbose_name=_('User'),
		blank=False,
		null=False,
		related_name='txu',
		on_delete=models.DO_NOTHING
	)
	current_date = models.DateTimeField(auto_now_add=True)
	formation_dar = models.ForeignKey(
		FormationDar,
		verbose_name=_('Formation Dar'),
		blank=False,
		null=False,
		related_name='txf',
		on_delete=models.DO_NOTHING
	)
	panier = models.ForeignKey(
		Panier,
		verbose_name=_('Panier'),
		blank=False,
		null=False,
		related_name='txp',
		on_delete=models.DO_NOTHING
	)

	def __str__(self):
		return '{0}'.format(self.panier)


class CodePromotion(models.Model):
	_uuid = models.UUIDField(unique=True, default= uuid4, editable=False)
	code_promotion = models.CharField(verbose_name=_('Code réduction'), max_length=200)
	percent_reduced = models.FloatField(verbose_name=_('Pourcentage de réduction'), default=0.0)
	still_valid = models.BooleanField(verbose_name=_('Encore valid'), default=False)
	date_debut = models.DateTimeField(blank=True)
	date_fin = models.DateTimeField(blank=True)

	def __str__(self):
		return '{0} - {1}%'.format(
			self.code_promotion,
			self.percent_reduced,
		)


class Promotion(models.Model):
	'''
	Les promotions offertes par Dar Blockchain
	@param: abonnement: Un ForeignKey avec Abonnement -> Relation Many to One
	@param: price_reduced: Réduction des prix lors d'une promotion
	'''
	_uuid = models.UUIDField(unique=True, default= uuid4, editable=False)
	dar = models.ForeignKey(
		Dyar,
		verbose_name=_('Dar'),
		null=False,
		blank=False,
		on_delete=models.DO_NOTHING,
		related_name='promd'
		)
	code_promotion = models.ForeignKey(
		CodePromotion,
		verbose_name=_('Code Promotion'),
		null=False,
		blank=False,
		on_delete=models.DO_NOTHING,
		related_name='promc'
		)
	reservation = models.ForeignKey(
		Reservation,
		verbose_name=_('Reservation'),
		null=True,
		blank=True,
		on_delete=models.DO_NOTHING,
		related_name='promres'
		)

	produit = models.ForeignKey(
		Produit,
		verbose_name=_('Produit'),
		blank=True,
		null=True,
		on_delete=models.DO_NOTHING,
		related_name='promp'
		)

	def __str__(self):
		return '{0}'.format(self.code_promotion)




	

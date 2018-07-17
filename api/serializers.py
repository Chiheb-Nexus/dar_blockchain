from rest_framework import serializers
from django.core.exceptions import ValidationError
from dar.models import (
	DarUser, 
	Dyar, 
	Salle, 
	Produit, 
	Reservation, 
	Panier, 
	Transaction,
	ProduitSalle,
	FormationDar,
	TransactionFormation
	)
from django.utils.translation import gettext as _
from rest_framework_jwt.settings import api_settings

class UserSerializer(serializers.RelatedField):
	'''
	Serialize user in DarUser model
	'''
	def to_representation(self, value):
		'''
		Return User's username & email
		'''
		return {
			"username": value.username, 
			"email": value.email if value.email else None
		}


class DarUserSerializer(serializers.ModelSerializer):
	'''
	Serialize DarUser model
	'''
	user = UserSerializer(read_only=True)
	uuid = serializers.CharField(source='_uuid')


	class Meta:
		model = DarUser
		fields = ('uuid', 'user', 'solde', 'tel', 'public_address')


class DyarSerializer(serializers.ModelSerializer):

	class Meta:
		model = Dyar
		fields = ('__all__')


class DarInfoSerializer(serializers.ModelSerializer):
	'''
	Serialize Dar
	@param: admin: Admin de la salle
	@param: uuid de la salle
	@param: fonction de la salle
	'''
	admin = serializers.CharField()
	uuid = serializers.CharField()
	fonction = serializers.CharField()
	id_salle = serializers.CharField()

	class Meta:
		model = Dyar
		fields = ('admin', 'uuid', 'fonction', 'id_salle')


class SalleProduitSerializer(serializers.ModelSerializer):
	product = serializers.CharField()
	desc = serializers.CharField()
	uuid = serializers.CharField()

	class Meta:
		model = ProduitSalle
		fields = ('uuid', 'desc', 'product')



class Produit_serializer(serializers.ModelSerializer):
	
	class Meta:
		model = Produit
		exclude = ('salle',)


class Panier_serializers(serializers.ModelSerializer):

	class Meta:
		model = Panier
		fields = ('montant','date','tx_hash','_uuid')


class Produit_transaction_serializer(serializers.RelatedField):
	'''
	Serialize Produit in Transaction model
	'''
	def to_representation(self, value):
		'''
		Return product's name & price
		'''
		return {
			"nom_produit": value.nom,
			"price"		 : value.price
		}

class ProduitSalleSerialiezers(serializers.ModelSerializer):
	
	uuid = serializers.CharField()
	product  = serializers.CharField()
	desc   = serializers.CharField()
	price		 = serializers.FloatField()
	quantity	 = serializers.IntegerField()

	class Meta:
		model = ProduitSalle
		fields= ('uuid','product','desc','price','quantity')

class FormationSerializers(serializers.ModelSerializer):
	uuid = serializers.UUIDField()
	place = serializers.IntegerField()
	titre = serializers.CharField()
	desc   = serializers.CharField()
	date_debut_h = serializers.DateTimeField()
	date_fin_h   = serializers.DateTimeField()
	date_debut_y = serializers.DateField()
	date_fin_y	 = serializers.DateField()
	price = serializers.FloatField()
	
	class Meta:
		model = FormationDar
		fields = ('uuid','titre','desc','date_debut_h','date_debut_y','date_fin_h','date_fin_y','place','nb_place','price')
	


class AddSoldeSerializers(serializers.ModelSerializer):

	uuid  = serializers.UUIDField()
	class Meta:
		model = DarUser
		fields = ('solde','dar','uuid')


class GetSoldeSerializers(serializers.ModelSerializer):

	user = serializers.CharField()
	dar = serializers.CharField()
	class Meta:

		model= DarUser
		fields = ('user','dar')
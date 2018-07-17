from django.views import View
from django.contrib.auth import authenticate
from dar.forms.Form_login import Form_login
from dar.forms.Form_register import Form_register
from django.urls import reverse
from django.contrib.auth.models import User
import django.db.utils as djExceptions
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from dar import models
from api import serializers , permissions
from django.middleware.csrf import get_token
from django.utils.translation import gettext as _
from django.db.models import Count
from django.db.models import F, Q ,When, Case
import uuid
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import exceptions
from rest_framework import status
from itertools import chain
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from collections import defaultdict
from django.db import transaction as t_atomic
from dar.smart_contract.InteractionWithUser import InteractionWithUser
from dar.utils.register_user import RegisterUser
from rest_framework.authtoken.models import Token
from rest_framework_jwt.settings import api_settings
from collections import OrderedDict
from django.db.models.functions import Trunc
from django.db.models import DateTimeField
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from django.utils import timezone  
from django.utils import timezone


import json

from django.db.models.functions import Trunc
from django.db.models import DateTimeField   
from django.utils import timezone


class CsrfExemptSessionAuthentication(SessionAuthentication):
	def enforce_csrf(self, request):
		return
class Login(generics.GenericAPIView):
	

	def post(self,request,*args,**kwargs):
		elems = ["username", "password"]
		if not all(map(lambda x: x in elems, request.data)):
			raise exceptions.ValidationError(_('missed Value'))
		user = authenticate(username=username, password=password) 
		if user is None:
			print("error login")
			raise exceptions.AuthenticationFailed(_("Authentification Failed"))
		try:
			user = models.DarUser.objects.get(user=user)

		except models.DarUser.DoesNotExist as e:
			print(e)
			raise exceptions.ValidationError(_('user does not exist'))

class UserInformations(APIView):
	'''
	 
	'''
	
	serializer_class = serializers.ProduitSalleSerialiezers

	def get(self, request, version):
		return Response({'detail': _('You can only POST')})

	def post(self, request, format=None):
		'''
		Retourner les informations de l'utilisateur.
	
		
		Exemple: {"username": "hello", "password": "hii"}
		'''
		username = request.data.get("username")
		password = request.data.get("password")
		user = authenticate(username=username, password=password)
	
		if user:
			dar_user = models.DarUser.objects.get(user=user)
			return Response(serializers.DarUserSerializer(dar_user).data)

		return Response({"detail": _('User not found')}, status=status.HTTP_400_BAD_REQUEST)

class getToken(APIView):
	
		def get(self, request):
			current_user = request.user
			jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
			jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
			payload = jwt_payload_handler(current_user)
			token = jwt_encode_handler(payload)
			return Response({"token":token})

class Register(APIView):
	serializer = serializers.DarUserSerializer
	permission_classes = ( permissions.AllowAny,)
	def post(self, request, format=None):
		'''
		@POST
		Exemple: {}
		Return l'objet de l'utilisateur crée.
		Return Token (JWT)
		Exemple: {_uuid: xxx, user: yyy, solde: zz.zz, tel: mm,
					public_address: 0x..,token: xXxXxX}
		
		@RegisterUser class 
		@register() function in register
		'''
		password = request.data.get('password')
		username = request.data.get('username')
		email = request.data.get('email')
		telephone = request.data.get('tel')
		dar = request.data.get('dar')

		if not password or not username or not email or not telephone or not dar:
			raise exceptions.AuthenticationFailed(_('missed value'))
		try:
			
			serializer_value= RegisterUser(username=username,
				password=password, 
				email=email,
				telephone=telephone, dar=dar).register()
		except Exception as e:
			print(e)
			raise exceptions.AuthenticationFailed(_('error while save user'))

		if isinstance(serializer_value, models.DarUser):
			return Response(serializers.DarUserSerializer(serializer_value).data)
		return Response(serializer_value)


class DyarsAPI(generics.ListAPIView):
	serializer_class = serializers.DyarSerializer

	def get_queryset(self):
		range_min, range_max = self.kwargs.get('range_min', 0), self.kwargs.get('range_max', 50)
		queryset = models.Dyar.objects.all()[int(range_min):int(range_max)]
		
		return queryset


class DarInfoAPI(generics.ListAPIView):
	'''
	Return dar's salles info
	'''
	serializer_class = serializers.DarInfoSerializer

	def get_queryset(self):
		dar_uuid = self.kwargs.get('uuid_dar', None)
		print(self.kwargs)

		try:
			dar_uuid = uuid.UUID(dar_uuid)
		except Exception as e:
			print(e)
			raise exceptions.ParseError(_('dar UUID not valid'))

		range_min = self.kwargs.get('min', 0)
		range_max = self.kwargs.get('max', 50)

		try:
			query = models.Dyar.objects.get(_uuid=dar_uuid)
		except Exception as e:
			raise exceptions.NotFound(_('Cannot find dar with: {}'.format(str(dar_uuid))))

		queryset = query.spd.annotate(
			admin=F('user__user__username'),
			uuid=F('_uuid'), 
			fonction=F('fonction_salle__fonction_name'), 
			id_salle=F('nom_salle')
		)

		return queryset

class SalleProduitsAPI(generics.ListAPIView):
	'''
	@GET uuid_salle 
	return [produit/salle]
	'''
	serializer_class = serializers.ProduitSalleSerialiezers

	def get_queryset(self):
		print("uuid",self.kwargs.get('uuid_salle'))
		uuid_salle = self.kwargs.get('uuid_salle', None)
		
		try:
			query = models.ProduitSalle.objects.filter(salle___uuid=uuid.UUID(uuid_salle))
		except Exception as e:
			print(e)
			raise exceptions.ParseError(_('Salle UUID not valid'))

		queryset = query.annotate(product=F('produit__nom'),
    			uuid=F('produit___uuid'),
				desc=F('produit__description')
				).values('product','uuid','desc','price','quantity')

		return queryset

class TransactionAPI(APIView):
	'''

	Exemple : {
	"produit":[
			{"qte":1,"uuid":"uuid produit"},
		]
	"formation":[
			{"qte":1,"uuid":"uuid formation"}
	]
	}

	'''
	def calcul_formation(self,formation):
		arr_formation = defaultdict(int)
		for elm in formation:
			try:
				uuid.UUID(elm.get('uuid'))
			except ValueError as e:
				print(e)
				raise exceptions.ValidationError(_('invalid uuid'))
			arr_formation[elm.get('uuid')] += elm.get('qte')
		query = Q()
		query.connector = Q.OR
		for v_uuid, qte_form in arr_formation.items():
			query.add(Q(formation___uuid=uuid.UUID(v_uuid)) & Q(
				nb_place__gte=qte_form) & Q(
				date_debut__gte=timezone.now()), query.connector)
		formation_dispo = models.FormationDar.objects.filter(query)

		total = sum(formation_dispo.get(formation___uuid = uuid.UUID(uuid_form)).price *arr_formation[uuid_form] for uuid_form in arr_formation)
 
		return total ,arr_formation ,formation_dispo

	def calcul_produit(self,produit):
		arr_produit = defaultdict(int)

		for elm in produit:
			#verif uuid request data
			try:
				uuid.UUID(elm.get('uuid'))
			except ValueError as e:
				print(e)
				raise exceptions.ValidationError(_('invalid uuid'))
			arr_produit[elm.get('uuid')] += elm.get('qte')

		query = Q()
		query.connector = Q.OR
		for v_uuid, k_prod in arr_produit.items():
			query.add(Q(alimentation_produit__produit___uuid=uuid.UUID(v_uuid)) & Q(
				quantity__gte=k_prod), query.connector)

		try:
			produit_dispo = models.ProduitSalle.objects.filter(query).values("_uuid","alimentation_produit__produit___uuid","quantity","price")
		except Produit.DoesNotExist as e:
			print(e)
		except Exception as e:
			print(e)
			raise exceptions.ValidationError(_('invalid produit'))
		if not produit_dispo:
			raise exceptions.ValidationError(_('produit non trouve'))
		
		# return les produits indisponibles 
		if produit_dispo.count() != len(arr_produit) :
			uuid_products_non_dispo = [x.encode('utf8') for x in arr_produit for y in produit_dispo if x != str(y.get('produit___uuid'))]
			return Response(
				{'error':'produit non disponible',
				'prod_non_dispo':uuid_products_non_dispo}
			)
		total = 0

		# calcule total produit achete 
		total = sum(item.get('price') * arr_produit[itemm] for item in produit_dispo for itemm in arr_produit  if str(item.get('alimentation_produit__produit___uuid')) == itemm)
		return total , arr_produit,produit_dispo
		
	def post(self, request):
		print(request.data)
		'''
		Parse Transaction
		@arr_produit = array regroupe les produits et qte
		@arr_formation = array regroupe les formations et qte
		@elems		 = verif les elements from @param request.data
		@uuid_user,uudi_salle= les valeurs from @param request.data		
		@produit_dispo = array produit disponible (qte>) from DB
		@total 		 = montant total des produits
		@tx_hash = return function , transaction hash of transaction
		'''
		arr_produit = defaultdict(int)
		arr_formation = defaultdict(int)
		form = request.data.get('formation',None)
		prod = request.data.get('produit',None)
		totalFormation = 0;
		totalProduit = 0
		user = self.request.user
		if user is None:
			raise exceptions.NotAuthenticated(_('user not authent...'))
		try:
			#FIX ME
			user = models.DarUser.objects.select_related("dar").get(user=user)
			dar = user.dar

		except exceptions.ValidationError:
			print("invalid uuid user in serializers transaction")
			raise exceptions.ValidationError(_('invalid user'))
		except models.DarUser.DoesNotExist as e:
			print(e)
			raise exceptions.ValidationError(_('invalid user'))
		except Exception as e:
			print(e)
			raise exceptions.ValidationError(_('invalid information'))
		if form is None and prod is None:
			raise exceptions.ErrorDetail(_('error value'))
		if not form is None:
			totalFormation , arr_formation,formation_dispo = self.calcul_formation(form)
		if not prod is None:
			totalProduit ,arr_produit,produit_dispo = self.calcul_produit(prod)
		total = totalFormation + totalProduit

		print("total	:	",	total)
		total = int(total * 1000)
 
		interact = InteractionWithUser()
		try:
			tx = interact.transfer(user_from=user, value=total)
		except Exception as e:
			print(e)
			raise exceptions.ErrorDetail(_('solde insuffisant'))
		if tx is None:
			raise exceptions.APIException(_('Transaction failed'))
		# create panier
		pan = models.Panier(dar=dar, user=user, montant=total, tx_hash=tx)
		pan.save()
		if not form is None:
			# ajouter les formations a formationTransaction
			transactionFormation = [models.TransactionFormation(user=user,panier=pan,formation_dar=formation) for formation in formation_dispo]
			models.TransactionFormation.objects.bulk_create(transactionFormation)
			# update place formation
			try:
				with t_atomic.atomic():
					for arr in arr_formation:
						transForm = models.FormationDar.objects.get(formation___uuid= uuid.UUID(arr))
						transForm.place_restant += arr_formation[arr]
						transForm.save()
			except Exception as e :
				print(e)
				raise Exception(_('Error in Transaction'))

		if not prod is None:
			# ajouter les produits a une transaction
			query = Q()
			query.connector = Q.AND
			for item in produit_dispo:
				query.add(Q(alimentation_produit__produit___uuid=item.get('alimentation_produit__produit___uuid')), query.connector)

			produit_dispo_ = models.ProduitSalle.objects.filter(query)
			transaction = [models.Transaction(produit = prod, quantity = arr_produit[str(prod._uuid)],panier = pan) for prod in produit_dispo_]

			models.Transaction.objects.bulk_create(transaction)

			# update quantity product
			try:

				with t_atomic.atomic():
					prod_filtred = (
						(k, v) for k in produit_dispo 
							for j, v in arr_produit.items() 
								if k.get("alimentation_produit__produit___uuid") == uuid.UUID(j)
					)
					for prod_salle, value in prod_filtred:
						pp = models.ProduitSalle.objects.get(alimentation_produit__produit___uuid = prod_salle.get('alimentation_produit__produit___uuid'))
						pp.quantity -= value
						pp.save()
			except Exception as e:
				print(e)
				raise Exception(_('Error in Transaction'))
		print('tx_hash transaction',tx)
		return Response({'tx_hash': tx})


class AddSoldeAPI(generics.GenericAPIView):
	'''
		@POST
		Exemple : {user:e7c5f825-8259-4d71-b98a-9f965a61d665,
		dar:8320ff72-273f-47d8-8c2c-d0c4b1616e33,
		solde:3300000}
	'''
	serializer_class = serializers.AddSoldeSerializers
	def post(self, request,*args,**kwargs):
		
		elems = ["user", "dar","solde"]
		if not all(map(lambda x: x in elems, request.data)):
			raise exceptions.ValidationError(_('missed Value'))
		try:
			solde = int(request.data.get('solde',None))
		except ValueError as e:
			print(e)
			raise exceptions.ValidationError(_('invalid solde'))
		try:
			uuid_user = uuid.UUID(request.data.get('user', None))
			uuid_dar = uuid.UUID(request.data.get('dar',None))
		except ValueError as e:
			print(e)
			raise exceptions.ValidationError(_('invalid information'))
		
		try:
			user = models.DarUser.objects.select_related("dar").get(_uuid=uuid_user)

		except models.DarUser.DoesNotExist as e:
			print(e)
			raise exceptions.ValidationError(_('user does not exist'))
		print(uuid_dar)
		if not user.dar._uuid ==uuid_dar:
			raise exceptions.ValidationError(_('dar not matching'))
		
		try:
			interac = InteractionWithUser()
			tx_hash = interac.add_solde(user=user,value= solde)
			print(tx_hash)
			return Response({"tx_hash": tx_hash})
		except Exception as e:
			print(e)
			raise exceptions.ValidationError(_('invalid information'))

class GetSoldeAPI(generics.GenericAPIView):
	authentication_class = (JSONWebTokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	'''
	@POST
	{"user":"f8ad3780-db3d-4ffd-a83a-17238c5e4ccb","dar":"010b3718-5e7c-4864-87cc-1c85ee6ab6b2"}
	'''
	serializer_class = serializers.GetSoldeSerializers
	def post(self, request,*args,**kwargs):
		elems = ["user", "dar","solde"]
		if not all(map(lambda x: x in elems, request.data)):
			raise exceptions.ValidationError(_('missed Value'))
		try:
			uuid_user = uuid.UUID(request.data.get('user', None))
			uuid_dar = uuid.UUID(request.data.get('dar',None))
		except ValueError as e:
			print(e)
			raise exceptions.ValidationError(_('invalid information'))
		
		try:
			user = models.DarUser.objects.select_related("dar").get(_uuid=uuid_user)

		except models.DarUser.DoesNotExist  as e:
			print(e)
			raise exceptions.ValidationError(_('user does not exist'))

		if not user.dar._uuid ==uuid_dar:
			raise exceptions.ValidationError(_('dar not matching'))
		
		try:
			interac = InteractionWithUser()
			solde_sm, solde_db = interac.get_solde(user=user)
			return Response({"solde_sm": solde_sm, "solde_db": solde_db})
		except Exception as e:
			print(e)
			raise exceptions.ValidationError(_('error while adding solde'))


class Get_uuid(APIView):

	def get(self,request, version):
		uuid = request.session.get("uuid",None)
		return Response(uuid)

class Transaction_historique_all(generics.ListAPIView):
	'''
	tesst documentation
	parametre	
	@GET min / max
	return 
	[{montant , date , tx_hash,'_uuid panier}]
	'''
	serializer_class = serializers.Panier_serializers
	def get_queryset(self):
		current_user = self.request.user
		uuid_panier = self.kwargs.get("uuid-panier",None)
		range_max = int(self.kwargs.get("range_max",50))
		range_min = int(self.kwargs.get("range_min",0))

		if current_user is None:
			raise exceptions.AuthenticationFailed(_('user not found'))
		query = models.Panier.objects.filter(user__user=current_user).extra(
			select={'date':"to_char(date, 'YYYY-MM-DD HH24:MI')"}).values('tx_hash','date','montant','_uuid').order_by('-date')[range_min:range_max]
		
		return query


class TransactionByUUIDPanier(APIView):
	'''
	@GET uuid panier
 	return list {prix, nom_produit , quantiy} by uuid Panier
	'''

	def get(self, request, uuid_panier):
		try:
			uuidPanier = uuid.UUID(uuid_panier)
		except Exception as e:
			print(e)
			raise exceptions.ValidationError(_('invalid uuid panier'))

		try:
			queryset = models.Transaction.objects.filter(
				panier___uuid = uuidPanier
				).annotate(
					prix = F('produit__price'),
					nom = F('produit__alimentation_produit__produit__nom')
					).values('prix','nom','quantity')
			queryset_formation = models.TransactionFormation.objects.filter(
				panier___uuid = uuidPanier
				).annotate(
					prix = F('formation_dar__price'),
					nom = F('formation_dar__formation__titre'),
				).values('prix','nom')
			query = {
					'produits': [ obj for obj in queryset ], 
					'formations': [ obj for obj in queryset_formation ]
			}
		except Exception as e:
		
			print(e)
			raise exceptions.ValidationError(_('Error uuid'))
		if (queryset.count() + queryset_formation.count()) == 0:
			raise exceptions.NotFound(_("Pannier vide"))
		return Response(query)


class SalleProduit(APIView):

	def get(self,request,uuid_dar, version):
		
		
		try:
			uuid_darr = uuid.UUID(uuid_dar)
		except Exception as e:
			print(e)
			raise exceptions.ValidationError(_("invalid dar"))
		prod = {}
		for item in models.Salle.objects.filter(dar___uuid=uuid_darr):
				prod[str(item._uuid)] = list(item.prs.values('produit__nom','quantity','price'))
		
		return JsonResponse(prod)
				
class ProduitAll(generics.ListAPIView):
	
	serializer_class = serializers.ProduitSalleSerialiezers
	def get_queryset(self):
		print(self.request)
		try:
			current_user = self.request.user
			dar = models.DarUser.objects.get(user = current_user).dar 
		except Exception as e:
			print(e)
			raise exceptions.NotAuthenticated(_('user not found'))	
		queryset = models.ProduitSalle.objects.filter(salle__dar=dar,quantity__gte=0).annotate(
			product=F('alimentation_produit__produit__nom'),
			desc = F('alimentation_produit__produit__description'),
			uuid = F('alimentation_produit__produit___uuid'),
			).values(
				'product','price','quantity','desc','uuid'
			)
		return queryset

class FormationDar(generics.ListAPIView):
	'''
	'''
	serializer_class = serializers.FormationSerializers

	def get_queryset(self):
		
		try:
			cuurent_user = self.request.user
			dar = models.DarUser.objects.get(user = cuurent_user).dar
		except Exception as e:
			print(e)
			raise exceptions.NotAuthenticated(_('user not found'))
		queryset = models.FormationDar.objects.filter(salle__dar = dar).filter(date_debut__gte=timezone.now()).annotate(uuid = F('formation___uuid'),titre= F('formation__titre'),desc = F('formation__description'),place = F('nb_place') - F('place_restant')).extra(
		select={'date_debut_y':"to_char(date_debut, 'YYYY-MM-DD')", 'date_debut_h':"to_char(date_debut, 'HH24:MI')", 
		'date_fin_y':"to_char(date_fin, 'YYYY-MM-DD')", 'date_fin_h':"to_char(date_fin, 'HH24:MI')"}) .values('uuid','titre','desc','nb_place','date_debut_y',
		'date_debut_h','date_fin_y','date_fin_h','place','price')
		return queryset



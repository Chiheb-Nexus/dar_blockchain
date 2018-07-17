from django.urls import path, include, re_path
from api import views
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

app_name='api'

urlpatterns = [
	path(
		'user', 
		views.UserInformations.as_view(), 
		name='user_informations'
	),
	path(
		'register',
		views.Register.as_view(),
		name='register'
	),
	path(
		'dyars', 
		views.DyarsAPI.as_view(), 
		name='dyars_API'
	),
	re_path(
		r'dyars/min=(?P<range_min>(\d+))&max=(?P<range_max>(\d+))$', 
		views.DyarsAPI.as_view(), 
		name='dyars_API_range'
	),
	re_path(
		r'salles/dar=(?P<uuid_dar>[0-9a-z-A-Z-]+)$', 
		views.DarInfoAPI.as_view(), 
		name='salles_API'
	),
	re_path(
		r'salles/dar=(?P<uuid_dar>[0-9a-z-A-Z-]+)&min=(?P<range_min>(\d+))&max=(?P<range_max>(\d+))$', 
		views.DarInfoAPI.as_view(), 
		name='salles_API_ranges'
	),
	re_path(
		r'produits/salle=(?P<uuid_salle>[0-9-a-z-A-Z]+)$', 
		views.SalleProduitsAPI.as_view(), 
		name='salle_produit_API'
	),
	path (
		'transaction',
		views.TransactionAPI.as_view(),
		name='transaction'
	),
	path(
		'add-solde',
		views.AddSoldeAPI.as_view(),
		name='add_sodlde'
	),
	path(
		'get-solde',
		views.GetSoldeAPI.as_view(),
		name='get_solde'
	),

	re_path(r'^historique/min=(?P<range_min>(\d+))&max=(?P<range_max>(\d+))/?$',
		views.Transaction_historique_all.as_view(),name='transaction_historique'),

	path('uuid',views.Get_uuid.as_view(),name='uuid'),
	path('api-token-auth/', obtain_jwt_token),
	path('auth/refresh_token/', refresh_jwt_token),
	re_path(
		r'panier/uuid-panier=(?P<uuid_panier>[0-9-a-z-A-Z]+)$', 
		views.TransactionByUUIDPanier.as_view(), 
		name='transaction_panier_API'
	),
	path("get-token", views.getToken.as_view(), name="get_token"),


	path('produit',views.ProduitAll.as_view(),name='produit'),
	path('formation-dar',views.FormationDar.as_view(),name='formation-dar'),
	]

schema_view = get_swagger_view(title='Dar Blockchain API')
app_name='api-docs'

urlpatterns = urlpatterns + [
	path(
		'docs', 
		include_docs_urls(title='Dar Blockchain API', public=False),
		 name='docs'
	),
	path('swagger', 
		schema_view,
		 name='schema-js'
	),
]

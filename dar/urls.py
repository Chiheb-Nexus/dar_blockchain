#
# Dar Blockchain
#
# © Dar Blockchain:
#

from django.urls import path, include, re_path
from . import views

app_name = 'dar'
urlpatterns = [
	path('', views.Index.as_view(), name='index'),
	path('login', views.Login.as_view(), name='login'),
	path('register', views.Register.as_view(), name='register'),
	path('logout', views.Logout.as_view(), name='logout'),
	path('error', views.CustomError.as_view(), name='error'),
	path('salle', views.SalleDar.as_view(), name="salle"),
	re_path(
		r'produit/salle=(?P<uuid_salle>[0-9-a-z-A-Z]+)$', 
		views.ProduitSalle.as_view(), 
		name='salle_produit'
	),
	]
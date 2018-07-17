#
# Dar Blockchain 
#
# © Dar Blockchain:
#

from django.shortcuts import render, Http404, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from dar.forms.Form_login import Form_login
from dar.forms.Form_register import Form_register
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from dar import models
from dar.utils.register_user import RegisterUser
from django.db.models import F
import uuid
from rest_framework_jwt.settings import api_settings

__authors__ = ['Chiheb Nexus', 'Mounir Ben Romdhane']


def get_token(obj):
	jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
	jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
	payload = jwt_payload_handler(obj)
	token = jwt_encode_handler(payload)
	return token

class Login(View):
	
	formLogin = Form_login
	def get(self,request):
		current_user = request.user
		if current_user.is_authenticated:
			return redirect(reverse('dar:index'))
		template = "backend_user/login.html"
		self.formLogin = Form_login()
		return render(request,template,{'form': self.formLogin})

	def post(self, request):
		form = self.formLogin(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)

			if user is not None:
				
				login(request, user)  
				resp = HttpResponseRedirect(reverse('dar:index'))
				resp.set_cookie('token', get_token(user))
				return resp
			else:
				return redirect(reverse('dar:error'))
		return HttpResponse("error")


class Logout(View):
	def get(self, request):
		django_logout(request)
		return redirect(reverse('dar:login'))


class Index(View):
	template = "backend_user/base.html"

	def get(self, request):
		current_user = request.user
		if current_user.is_authenticated:
			user = models.DarUser.objects.filter(user=current_user).first()
			
			return render(request, self.template, {'currentuser': user,'uuid':user._uuid,'uuiddar':user.dar._uuid})

		formLogin = Form_login()
		return render(request,"backend_user/login.html", {'form': formLogin})


class Register(View):

	template = "backend_user/register.html"
	formRegister = Form_register

	def get(self, request):
		return render (request,self.template,{'form':self.formRegister})

	def post(self, request):
		form = self.formRegister(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			tel = form.cleaned_data['telephone']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			dar = form.cleaned_data['dar']
			try:
				dar_user = RegisterUser(
							username=username, 
							password=password, 
							email = email, 
							telephone= tel,
							dar= dar).register()
			except IntegrityError as e:
				return render(request,self.templete, {
						'form':self.formRegister, 
						'errors': 'User already exist'
					})
			return redirect(reverse('dar:index'))
		else:
			return render(request, self.template, {'form' : form})



class CustomError(View):
	template = "backend_user/home.html"
	def get(self, request, *kawargs):
		return render(request, self.template	)

class ProduitSalle(View):
	
	def get(self,request,uuid_salle = None):
		
		try:
			query = models.ProduitSalle.objects.filter(salle___uuid=uuid.UUID(uuid_salle))
		except Exception as e:
			print(e)
			

		queryset = query.annotate(product=F('produit__nom'),
    			uuid=F('produit___uuid'),
				desc=F('produit__description')
				).values('product','uuid','desc','price','quantity')
		return render(request,"backend_user/home.html",{'prod':queryset})

class Test(View):
	def get(self, request):
		import random 
		return render(request, 'backend_user/test.html', {'val': request.user})
		

class SalleDar(View):
	template = "backend_user/salle.html"
	def get(self,request):
		
		current_user = request.user
		if current_user is None:
			redirect(reverse('dar:index'))
		salle = models.DarUser.objects.get(user=current_user).dar.spd.all().annotate(uuid=F('_uuid'))
		return render(request,self.template,{'salles':salle})


class ProduitSalle(View):
	
	def get(self,request , uuid_salle=0):
		try:
			uuid_salle = uuid.UUID(uuid_salle)
		except Exception as e:
			print(e)
		query = models.ProduitSalle.objects.filter(salle___uuid=uuid_salle)
		queryset = query.annotate(product=F('produit__nom'),
    			uuid=F('produit___uuid'),
				desc=F('produit__description')
				).values('product','uuid','desc','price','quantity')

		return render(request,"backend_user/produit-salle.html",{"produits":queryset})







#
# Dar Blockchain
#
# © Dar Blockchain:
#

from django import forms
from django.utils.translation import gettext as _

__authors__ = ['Chiheb Nexus', 'Mounir Ben Romdhane']

class Form_login(forms.Form):
	'''
	Le login de la form HTML
	@param: username: Username enregistré dans la DB : CharField
	@param: password: Password haché dans la DB : CharField
	'''
	username = forms.CharField(
		required = True,
		label = _('Username'),
		max_length = 32,
		widget = forms.TextInput(attrs={'class': "form-control", 'id': 'form_login_username'}),

        )    
	password = forms.CharField(
		label = _('Password'),
		max_length = 32,
		widget = forms.PasswordInput(
			attrs={'class' : "form-control", 'id': 'form_login_password'}),
		)



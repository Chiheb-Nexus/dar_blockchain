#
# Dar Blockchain
#
# © Dar Blockchain:
#

from django import forms
from dar import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.db.utils import ProgrammingError
from django.core.validators import RegexValidator
import uuid
__authors__ = ['Chiheb Nexus', 'Mounir Ben Romdhane']

def dyar_choices():
	try:
		CHOICES = ((k._uuid, k.nom) for k in models.Dyar.objects.all())
	except ProgrammingError as e:
		CHOICES = ()
	return CHOICES

class Form_register(forms.Form):
	'''
	Le register de la Form HTML
	@param: username: Username qui va etre enregistré dans la DB
	@param: email: E-mail (regex required)
	@param: password: (regex required)
	@param: confirm_password: (regex required)
	@param: telephone: (regex required)
	@param: dar: Les dars enregistrés dans la DB
	'''
	username = forms.CharField(
		required=True,
		label=_('username'),
		max_length= 10,
		widget = forms.TextInput(attrs={'class': "form-control", 'id': 'register-username'})
		)

	email = forms.EmailField(
		required=True,
		label=_('email'),
		widget = forms.TextInput(attrs={'class': "form-control", 'id': 'register-email'})
		)
	password = forms.CharField(
		required=True,
		label = _('Password'),
		max_length = 100,
		widget = forms.PasswordInput(attrs={'class' : "form-control", 'id': 'register-password'}),
		)
	confirm_password = forms.CharField(
		required=True,
		label = _('Confirm Password'),
		max_length = 100,
		widget = forms.PasswordInput(attrs={'class' : "form-control", 'id': 'register-confirm'}),
		)
	telephone = forms.CharField(
		required=True,
		label=_('Numero telephone'),
		max_length= 12,
		validators=[],
		widget = forms.TextInput(attrs={'class': "form-control", 'id': 'register-telephone'})
		)

	dar = forms.ChoiceField(label='Dar', choices=dyar_choices, required=True)


	def clean(self):
		'''
		Vérifie si les champs des mots de passes sont identiquess
		'''
		cleaned_data = super(Form_register, self).clean()
		password = cleaned_data.get("password")
		confirm_password = cleaned_data.get("confirm_password")
		if password != confirm_password:
			raise forms.ValidationError(_("Password and confirmed password did not match"))

	def clean_dar(self):
		cleaned_data = super(Form_register, self).clean()
		dar = cleaned_data.get('dar')
		print(dar)
		try :
			dar = uuid.UUID(dar)
		except ValueError as e:
			raise Exception('Not valid UUID')

		exist = models.Dyar.objects.filter(_uuid=dar).exists()
		if not exist:
			raise forms.ValidationError(_('Dar not valid'))
		return dar

		
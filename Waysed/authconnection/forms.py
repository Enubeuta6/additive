from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class RegisterUserForm(UserCreationForm):


    class Meta:
        model = UserDataMeta
        fields = ['username' ,'email',]



class LoginAccess(forms.ModelForm):
    class Meta:
        model = UserDataMeta
        fields = ['password', 'username']

class Generate(forms.ModelForm):
    class Meta:
        model = UserDataMeta
        fields = 'credit',
        widgets = {
        'credit': forms.NumberInput(attrs={'class': 'form-login'}),
        }
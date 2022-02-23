from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'input'}))
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'input'}))
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'class': 'input'}))

    class Meta:
        model = UserDataMeta
        fields = ('username' ,'email')



class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'input'}))


class Generate(forms.ModelForm):


    class Meta:
        model = PromoDataMeta
        fields = 'code_key',
        widgets = {
        'code_key': forms.TextInput(attrs={'class': 'form-login'}),
        }
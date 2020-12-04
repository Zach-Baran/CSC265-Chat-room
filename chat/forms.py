from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.db import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Profile, Chatroom, Messages


class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'formStyle', 'placeholder': 'Username', 'id': 'userID'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'formStyle',
            'placeholder': 'Password',
            'id': 'password1ID',
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'formStyle',
            'placeholder': 'Confirm Password',
            'id': 'password2ID',
        }
    ))


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'formStyle', 'placeholder': 'Username', 'id': 'userID'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'formStyle',
            'placeholder': 'Password',
            'id': 'passwordID',
        }
))



class ChatForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChatForm, self).__init__(*args, **kwargs)

    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'formStyle', 'placeholder': 'Chat name', 'id': 'nameID'}))
    token = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'formStyle',
            'placeholder': 'Token',
            'id': 'tokenID',
        }
    ))

    class Meta:
        model = Chatroom
        fields = ['name', 'token']


class SendMessage(forms.ModelForm):

    class Meta:
        model = Messages
        fields = ('content',)


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
        attrs={'class': 'formStyle', 'placeholder': 'Chat Name', 'id': 'nameID'}))

    class Meta:
        model = Chatroom
        fields = ['name', ]


class SendMessage(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SendMessage, self).__init__(*args, **kwargs)

    content = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'message-input ', 'placeholder': 'Enter a message...', 'id': 'sendID'}
    ))
    class Meta:
        model = Messages
        fields=['content']

class JoinChatForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(JoinChatForm, self).__init__(*args, **kwargs)

    token = forms.CharField(label='search', max_length=6, widget=forms.TextInput(attrs={'class': 'formStyle', 'placeholder': 'Input Chat Room Token'}))




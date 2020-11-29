from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, SendMessage
from .models import Messages
from django.contrib.auth.models import User

posts = [
    {
    'author':'testing',
    'content':'hhgfdhgfdhfgd',
    'date': '3/2/21'
    },
    {
    'author':'zach',
    'content':'321321321',
    'date':'3/21/23'
    }
]

def home(request):
    return render(request, 'chat/home.html')


def about(request):
    return render(request, 'chat/about.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            messages.success(request, f'Account created for {username}! Please login.')
            return redirect('chat-login')
    else:
        form = UserRegisterForm()
    return render(request, 'chat/register.html', {'form': form})


@login_required
def chatroom(request):
    tmp = Messages.objects.all()
    context = {
        'tmp': Messages.objects.all()
    }

    message = SendMessage(request.POST or None)
    if request.method=='POST':
        if message.is_valid():
            message.save()
    else:
        message = SendMessage()

    return render(request, 'chat/chatroom.html', {'context':tmp,'message':message})

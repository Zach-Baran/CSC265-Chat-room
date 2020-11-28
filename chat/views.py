from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import Messages
from django.contrib.auth.models import User



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
    users = {
        'users': User.objects.all()
    }
    messages = {
        'messages': Messages.objects.all()
    }

    return render(request, 'chat/chatroom.html', messages)

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm

# Create your views here.


def home(request):
    return render(request, 'chat/home.html')


def about(request):
    return render(request, 'chat/about.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            messages.success(request, f'Account created for {username}! Please login.')
            return redirect('chat-login')
    else:
        form = UserCreationForm()
    return render(request, 'chat/register.html', {'form': form})

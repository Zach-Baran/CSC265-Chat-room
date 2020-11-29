from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm
from .models import Messages, Chatroom
from django.contrib.auth.models import User


class HomeListView(LoginRequiredMixin, ListView):
    model = Chatroom
    template_name = 'chat/home.html'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        return user.chatroom_set.all()


class ChatDetailView(DetailView):
    model = Chatroom
    template_name = 'chat/chatroom.html'

    def get_context_data(self, **kwargs):
        context = super(ChatDetailView, self).get_context_data(**kwargs)

        # Query Messages
        id = self.kwargs.get('pk')
        chat = Chatroom.objects.get(id=id)
        chat_messages = chat.messages_set.all()

        context['chat_messages'] = chat_messages
        return context


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
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, FormView
from django.views.generic.detail import  SingleObjectMixin
from django.views.generic.edit import FormMixin, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.hashers import check_password
from .forms import UserRegisterForm, ChatForm, SendMessage, JoinChatForm
from .models import Messages, Chatroom
from .utils import AjaxableResponseMixin
from django.contrib.auth.models import User


class HomeListView(LoginRequiredMixin, ListView):
    model = Chatroom
    template_name = 'chat/home.html'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        return user.subscribed_to.all()


class ChatDisplay(LoginRequiredMixin,UserPassesTestMixin, DetailView):
    model = Chatroom
    template_name = 'chat/chatroom.html'
    slug_field = 'token'
    slug_url_kwarg = 'token'

    # denies entry to none subscribers of the chat
    def test_func(self):
        chat = self.get_object()
        if self.request.user in chat.subscribers.all():
            return True

    def get_context_data(self, **kwargs):
        context = super(ChatDisplay, self).get_context_data(**kwargs)

        # Obtain Chatroom Object
        token = self.kwargs.get('token')
        chat = Chatroom.objects.get(token=token)

        # Query Messages
        chat_messages = chat.messages_set.all()

        # Query Chat Users
        chat_users = chat.subscribers.all()

        context['chat_messages'] = chat_messages
        context['chat_users'] = chat_users
        context['form'] = SendMessage()
        return context


class ChatFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    template_name = 'chat/chatroom.html'
    form_class = SendMessage
    model = Chatroom
    slug_field = 'token'
    slug_url_kwarg = 'token'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('chat-chatroom', kwargs={'token': self.object.token})

    def form_valid(self, form):
        # Obtain Chatroom Object
        token = self.kwargs.get('token')
        chat = Chatroom.objects.get(token=token)

        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.chatroom = chat
        comment.save()

        ser_instance = serializers.serialize('json', [comment, ])

        # return super(ChatFormView,self).form_valid(form)
        return JsonResponse({"instance": ser_instance}, status=200)


# Get Requests gets the ChatDisplay View, Post Requests get the FormView
class ChatDetail(View):
    def get(self, request, *args, **kwargs):
        view = ChatDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ChatFormView.as_view()
        return view(request, *args, **kwargs)



class ChatCreateView(LoginRequiredMixin, CreateView):
    model = Chatroom
    form_class = ChatForm
    template_name = 'chat/chatroom-create.html'
    slug_field = 'token'
    slug_url_kwarg = 'token'

    # Setting the Chat Room Host and Subscriber
    def form_valid(self, form):
        form.instance.host = self.request.user
        obj = form.save(commit=True)

        # adds the user to the subscribers list
        obj.subscribers.add(self.request.user)
        obj.save()
        return super().form_valid(form)


class ChatUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Chatroom
    template_name = 'chat/chatroom-update.html'
    fields = ['name', 'password']
    slug_field = 'token'
    slug_url_kwarg = 'token'

    def get_form(self, form_class=JoinChatForm):
        form = form_class
        return form

    def test_func(self):
        chat = self.get_object()
        if chat.host == self.request.user:
            return True


class ChatDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Chatroom
    template_name = 'chat/chatroom-confirm-delete.html'
    success_url = '/'
    slug_field = 'token'
    slug_url_kwarg = 'token'

    def test_func(self):
        chat = self.get_object()
        if chat.host == self.request.user:
            return True




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
  

def ajax_process(request, **kwargs):
    token = kwargs.get('token')
    chat = Chatroom.objects.get(token=token)
    chat_messages = chat.messages_set.all()
    allData = []
    for message in chat_messages:
        string = str(message.date)
        timestamp = string[11:19]
        data = {
            'content' : message.content,
            'author' : message.author.username,
            'date' : timestamp,
            'id' : message.id
        }
        allData.append(data)

    return JsonResponse(allData, safe=False)

def messageProcess(request, **kwargs):
    print('ayo')

@login_required()
def joinChat(request):
    if request.method == 'POST':
        form = JoinChatForm(request.POST)
        if form.is_valid():
            chat = Chatroom.objects.get(token=form.cleaned_data['token'])
            if form.cleaned_data['password'] == chat.password:
                chat.subscribers.add(request.user)
                return redirect('chat-chatroom', chat.token)
            else:
                messages.success(request, f"Wrong Chatroom Token or Password.")
                return render(request, 'chat/chatroom-join.html', context={'form': form})
    else:
        form = JoinChatForm()
    return render(request, 'chat/chatroom-join.html', context={'form': form})


@login_required()
def leaveChat(request, token):
    user = request.user
    chat = Chatroom.objects.get(token=token)
    chat.subscribers.remove(user)
    messages.success(request, f'You have left {chat.name}!')
    return redirect('chat-home')

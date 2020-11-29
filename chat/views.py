from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserRegisterForm, ChatForm, SendMessage
from .models import Messages, Chatroom
from django.contrib.auth.models import User


class HomeListView(LoginRequiredMixin, ListView):
    model = Chatroom
    template_name = 'chat/home.html'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        return user.chatroom_set.all()


class ChatDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Chatroom
    template_name = 'chat/chatroom.html'

    # denies entry to none subscribers of the chat
    def test_func(self):
        chat = self.get_object()
        if self.request.user in chat.subscribers.all():
            return True

    # modifies the context dictionary
    def get_context_data(self, **kwargs):
        context = super(ChatDetailView, self).get_context_data(**kwargs)

        # Obtain Chatroom Object
        id = self.kwargs.get('pk')
        chat = Chatroom.objects.get(id=id)

        # Query Messages
        chat_messages = chat.messages_set.all()

        # Query Chat Users
        chat_users = chat.subscribers.all()

        context['chat_messages'] = chat_messages
        context['chat_users'] = chat_users
        return context


class ChatCreateView(LoginRequiredMixin, CreateView):
    model = Chatroom
    form_class = ChatForm
    template_name = 'chat/chatroom-create.html'

    # Setting the Chat Room Host and Subscriber
    def form_valid(self, form):
        form.instance.host = self.request.user
        obj = form.save(commit=True)

        # adds the user to the subscribers list
        obj.subscribers.add(self.request.user)
        obj.save()
        return super().form_valid(form)


class ChatUpdateView(LoginRequiredMixin, UpdateView):
    model = Chatroom
    template_name = 'chat/chatroom-update.html'
    fields = ['title']


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
  
  
# @login_required
# def chatroom(request):
#     tmp = Messages.objects.all()
#     context = {
#         'tmp': Messages.objects.all()
#     }

#     message = SendMessage(request.POST or None)
#     if request.method=='POST':
#         if message.is_valid():
#             message.save()
#     else:
#         message = SendMessage()

#     return render(request, 'chat/chatroom.html', {'context':tmp,'message':message})

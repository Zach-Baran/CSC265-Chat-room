from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin
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
        return user.subscribed_to.all()


class ChatDetailView(LoginRequiredMixin, UserPassesTestMixin, FormMixin, DetailView):
    model = Chatroom
    template_name = 'chat/chatroom.html'
    form_class = SendMessage

    # denies entry to none subscribers of the chat
    def test_func(self):
        chat = self.get_object()
        if self.request.user in chat.subscribers.all():
            return True

    def get_success_url(self):
        return reverse_lazy('chat-chatroom', kwargs={'pk': self.object.pk})

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
        context['form'] = self.get_form()
        return context

    def post(self,request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Obtain Chatroom Object
        id = self.kwargs.get('pk')
        chat = Chatroom.objects.get(id=id)

        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.chatroom = chat
        comment.save()

        return super(ChatDetailView,self).form_valid(form)


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
  

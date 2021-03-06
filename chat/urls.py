from django.urls import path
from django.contrib.auth import views as auth_views
from chat.forms import UserLoginForm
from . import views
from .views import *

urlpatterns = [
    path('', HomeListView.as_view(), name='chat-home'),
    path('about/', views.about, name='chat-about'),
    path('register/', views.register, name='chat-register'),
    path('login/', auth_views.LoginView.as_view(template_name='chat/login.html', authentication_form=UserLoginForm), name='chat-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='chat/logout.html'), name='chat-logout'),
    path('chatroom/<str:token>/', ChatDetail.as_view(), name='chat-chatroom'),
    path('chatroom/<slug:token>/update/', ChatUpdateView.as_view(), name='chat-chatroom-update'),
    path('chatroom/<slug:token>/delete/', ChatDeleteView.as_view(), name='chat-chatroom-delete'),
    path('chatroom/<slug:token>/leave/', views.leaveChat, name='chat-chatroom-leave'),
    path('join/', views.joinChat, name='chat-chatroom-join'),
    path('create/', ChatCreateView.as_view(), name='chat-create'),
    path('chatroom/<str:token>/query/', views.ajax_process, name='chat-get-messages'),
    path('chatroom/<str:token>/send/', views.messageProcess, name='chat-send-message')

]

from django.urls import path
from django.contrib.auth import views as auth_views
from chat.forms import UserLoginForm
from . import views

urlpatterns = [
    path('', views.home, name='chat-home'),
    path('about/', views.about, name='chat-about'),
    path('register/', views.register, name='chat-register'),
    path('login/', auth_views.LoginView.as_view(template_name='chat/login.html', authentication_form=UserLoginForm), name='chat-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='chat/logout.html'), name='chat-logout'),
    path('chatroom/',views.chatroom, name='chat-chatroom'),
]

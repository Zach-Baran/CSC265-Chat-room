from django.contrib import admin
from .models import Profile, Chatroom, Messages

# Register your models here.
admin.site.register(Profile)
admin.site.register(Chatroom)
admin.site.register(Messages)

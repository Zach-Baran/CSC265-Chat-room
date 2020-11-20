from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    #TODO Profile image
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class Chatroom(models.Model):
    host = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    token = models.CharField(max_length=6,null= False)
    date = models.DateTimeField(default=timezone.now)


class Messages(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    date = models.DateTimeField(default=timezone.now)
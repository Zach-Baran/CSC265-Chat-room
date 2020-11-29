from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    #TODO Profile image
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class Chatroom(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(User, blank=True, related_name='subscribed_to')
    name = models.CharField(max_length=25, null=False)
    token = models.CharField(max_length=6, null=False)
    date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('chat-chatroom', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.name}'


class Messages(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    date = models.DateTimeField(default=timezone.now)



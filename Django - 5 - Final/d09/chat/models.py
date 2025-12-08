from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

class ConnectedUser(models.Model):
    room = models.ForeignKey(Room, related_name='connected_users', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='connected_users', on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=255)

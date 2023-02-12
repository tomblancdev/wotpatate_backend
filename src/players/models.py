from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    account_id = models.IntegerField(primary_key=True, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.user.username


class PlayerToken(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.player.user.username

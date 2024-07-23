from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=50, default='null')
    setting = models.CharField(max_length=100, default='null')
    last_response = models.TextField(default="")

    def __str__(self):
        return self.name
    


class Character(models.Model):
    GENDER_CHOICES = {
        'male' : 'male',
        'female' : 'female',
        'other' : 'other',
    }

    name = models.CharField(max_length=50, default='null')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    hp = models.IntegerField(default=-1)
    origin = models.CharField(max_length=50)
    gender = models.CharField(max_length = 6, choices = GENDER_CHOICES, default = 'male')
    is_user = models.BooleanField(default=False)
    plot = models.CharField(max_length=500, default='defaultplot')
    stat = models.JSONField(default=list)
    items = models.JSONField(default=dict)

    def __str__(self):
        return self.name
    

class Log(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    

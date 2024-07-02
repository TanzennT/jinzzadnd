from django.db import models

# Create your models here.

class Game(models.Model):
    name = models.CharField(max_length=50, default='null')
    setting = models.CharField(max_length=100, default='null')

    def __str__(self):
        return self.name
    


class Character(models.Model):
    ORIGIN_CHOICES = {
        'dummy' : 'dummy'
    }

    GENDER_CHOICES = {
        'male' : 'male',
        'female' : 'female',
        'other' : 'other',
    }

    name = models.CharField(max_length=50, default='null')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    origin = models.CharField(max_length = 7, choices=ORIGIN_CHOICES, default = 'dummy')
    gender = models.CharField(max_length = 6, choices = GENDER_CHOICES, default = 'male')
    is_user = models.BooleanField(default=False)
    plot = models.CharField(max_length=500, default='defaultplot')
    stat = models.JSONField(default=dict)

    def __str__(self):
        return '{self.game.name}\s character'
    

class Log(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    

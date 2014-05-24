from django.db import models

# Create your models here.

class Survey(models.Model):
    ip = models.CharField(max_length=100, blank=True)  #
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)  #
    srid = models.CharField(max_length=100, unique=True)  #
    identity = models.CharField(max_length=100, blank=True)  #
    telephone = models.CharField(max_length=100, blank=True)  #
    answer1 = models.CharField(max_length=100, blank=True)  #
    answer2 = models.CharField(max_length=100, blank=True)  #
    answer3 = models.CharField(max_length=100, blank=True)  #
    answer4 = models.CharField(max_length=100, blank=True)  #
    answer5 = models.CharField(max_length=100, blank=True)  #
    answer6 = models.CharField(max_length=100, blank=True)  #
    location = models.CharField(max_length=200, blank=True)  #

    reward = models.BooleanField(default=False)
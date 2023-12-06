from django.db import models


# Create your models here.

class ProfileModel(models.Model):
    lastname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

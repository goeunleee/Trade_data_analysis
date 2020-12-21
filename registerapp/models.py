from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    com_name = models.CharField(max_length=255)
    com_major = models.CharField(max_length=255)
    
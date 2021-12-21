from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=12)

    def __str__(self):
        return self.username
    

class Company(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class Profile(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
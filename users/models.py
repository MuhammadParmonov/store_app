from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=15)
    profile = models.ImageField(upload_to="profile_images/", default="default_user.png")
    
    def __str__(self):
        return self.username
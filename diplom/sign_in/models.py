from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError


# Create your models here.
class CustomUser(AbstractUser):
    birthdate = models.DateField(null=True, blank=True)
    

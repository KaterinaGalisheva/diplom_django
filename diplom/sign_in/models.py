from django.contrib.auth.models import AbstractUser
from django.db import models
from asgiref.sync import sync_to_async

# Create your models here.
class CustomUser(AbstractUser):
    
    pass
    
    
# Асинхронная функция для получения данных из базы данных
@sync_to_async
def get_users_from_db():
    return list(CustomUser.objects.all())

@sync_to_async
def get_user_from_db(user_id):
    return CustomUser.objects.get(id=user_id)

@sync_to_async
def delete_user(user):
    user.delete()

@sync_to_async
def save_user(user):
    user.save()

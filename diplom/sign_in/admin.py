from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
 


# Register your models here.

#  в декораторе автоматически регистрируете модель с классом админки
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email')
    list_display_links = ('id', 'username', 'email')


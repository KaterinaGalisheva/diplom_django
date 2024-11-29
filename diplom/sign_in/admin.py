from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
 


# Register your models here.

#  в декораторе автоматически регистрируете модель с классом админки
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Добавляем поле для регистрации
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('birthdate',)}),  
    )
    # Добавляем поле для редактирования
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('birthdate',)}),  
    )


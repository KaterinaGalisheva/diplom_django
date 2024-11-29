from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

# Register your models here.
# Админка для модели spacestore
@admin.register(Spacestore)
class SpacestoreAdmin(admin.ModelAdmin):
    # Поля для отображения в списке
    list_display = ('title', 'description', 'size','cost', 'photo_display')
    # Поля для поиска
    search_fields = ('title', 'cost')
    # Фильтры
    list_filter = ('cost',)
    # Сортировка
    ordering = ('title',)
    # Форма для редактирования
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'size','cost', 'photo')
        }),
    )

    # Отображение изображения в списке
    def photo_display(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" style="width: 50px; height: auto;" />')
        return "Нет изображения"
    photo_display.short_description = 'Фото'

from django.contrib import admin
from .models import Post, Comment



# Register your models here    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'slug', 'publish', 'status')
    list_filter = ('status', 'created', 'publish')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug' : ('title', )}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email','body' )
    


from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'status']


class BlockUserAdmin(admin.ModelAdmin):
    list_display = ['username']
    list_filter = ['username']
    list_editable = ['username']

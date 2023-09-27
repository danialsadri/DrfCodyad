from django.contrib import admin
from .models import Article, BlockUser


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'status']


@admin.register(BlockUser)
class BlockUserAdmin(admin.ModelAdmin):
    list_display = ['username']
    list_filter = ['username']

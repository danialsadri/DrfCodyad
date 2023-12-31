from django.contrib import admin
from .models import Article, BlockUser, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'created', 'status']


@admin.register(BlockUser)
class BlockUserAdmin(admin.ModelAdmin):
    list_display = ['username']
    list_filter = ['username']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'created']
    list_filter = ['created']
    search_fields = ['description']
    raw_id_fields = ['article']

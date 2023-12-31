from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to="article/images", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class BlockUser(models.Model):
    username = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.username


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    description = models.TextField(max_length=500)
    created = models.DateField()

    def __str__(self):
        return self.description[:20]

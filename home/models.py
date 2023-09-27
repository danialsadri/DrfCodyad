from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title

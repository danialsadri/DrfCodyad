from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title

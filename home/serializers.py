from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Article


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ArticleSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(write_only=True)

    class Meta:
        model = Article
        fields = "__all__"

    def validate_title(self, value):
        if value == 'hello world':
            raise serializers.ValidationError('you can not choose a hello world')
        return value

    def validate(self, attrs):
        if attrs['title'] == attrs['description']:
            raise serializers.ValidationError('title and description can not be same')
        return attrs

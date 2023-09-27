from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Article, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


# def check_title(value):
#     if value == 'hello world':
#         raise serializers.ValidationError('tite can not be hello world')

# def check_title(value):
#     if value['title'] == 'hello world':
#         raise serializers.ValidationError('tite can not be hello world')

# def check_title(value):
#     if value['title'] == 'hello world':
#         raise serializers.ValidationError({'title': 'tite can not be hello world'})

class CheckTitle:
    def __call__(self, value):
        if value['title'] == 'hello world':
            raise serializers.ValidationError({'title': 'tite can not be hello world'})


class ArticleSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(write_only=True)

    class Meta:
        model = Article
        fields = "__all__"
        # validators = [check_title]
        validators = [CheckTitle()]
        # extra_kwargs = {
        #     'title': {'validators': [check_title]},
        # }

    # def validate_title(self, value):
    #     if value == 'hello world':
    #         raise serializers.ValidationError('you can not choose a hello world')
    #     return value

    # def validate(self, attrs):
    #     if attrs['title'] == attrs['description']:
    #         raise serializers.ValidationError('title and description can not be same')
    #     return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return Article.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

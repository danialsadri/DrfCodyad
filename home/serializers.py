from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework import serializers
from .models import Article, Comment
from persiantools.jdatetime import JalaliDate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class CommentSerializer(serializers.ModelSerializer):
    days_ago = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'article', 'description', 'created', 'days_ago']

    def get_days_ago(self, obj):
        return (now().date() - obj.created).days

    def get_created(self, obj):
        date = JalaliDate(obj.created, locale='fa')
        return date.strftime("%c")


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
    comments = serializers.SerializerMethodField()

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

    def get_comments(self, obj):
        article_serializer = CommentSerializer(instance=obj.comments.all(), many=True).data
        return article_serializer

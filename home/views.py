from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Article
from .serializers import UserSerializer, ArticleSerializer
import requests


class MessageView(APIView):
    def get(self, request: Request):
        name = request.query_params.get('name')
        return Response(data={'message': f"hello {name}"})

    def post(self, request: Request):
        name = request.data.get('name')
        return Response(data={'message': f"hello {name}"})


class GetCryptoPrice(APIView):
    def get(self, request: Request):
        coin = request.query_params.get('coin')
        response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={coin.upper()}")
        data = response.json()
        result = {
            'price': data['price'],
            'symbol': data['symbol']
        }
        return Response(data=result)


class UserListView(APIView):
    def get(self, request: Request):
        users = User.objects.all()
        user_serializer = UserSerializer(instance=users, many=True)
        return Response(data=user_serializer.data, status=status.HTTP_200_OK)


class ArticleListView(APIView):
    def get(self, request: Request):
        articles = Article.objects.all()
        article_serializer = ArticleSerializer(instance=articles, many=True)
        return Response(data=article_serializer.data, status=status.HTTP_200_OK)


class ArticleDetailView(APIView):
    def get(self, request: Request, post_id):
        article = Article.objects.get(id=post_id)
        article_serializer = ArticleSerializer(instance=article)
        return Response(data=article_serializer.data, status=status.HTTP_200_OK)


class ArticleCreateView(APIView):
    def post(self, request: Request):
        article_serializer = ArticleSerializer(data=request.data, context={'request': request})
        if article_serializer.is_valid():
            # if request.user.is_authenticated:
            #     article_serializer.validated_data['user'] = request.user
            article_serializer.save()
            return Response(data=article_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleUpdateView(APIView):
    def put(self, request: Request, post_id):
        article = Article.objects.get(id=post_id)
        article_serializer = ArticleSerializer(instance=article, data=request.data, partial=True)
        if article_serializer.is_valid():
            article_serializer.save()
            return Response(data=article_serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ArticleUpdateView(APIView):
#     def put(self, request: Request, post_id):
#         article = Article.objects.get(id=post_id)
#         article_serializer = ArticleSerializer(data=request.data, partial=True)
#         if article_serializer.is_valid():
#             article_serializer.update(instance=article, validated_data=article_serializer.validated_data)
#             return Response(data=article_serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(data=article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDeleteView(APIView):
    def delete(self, request: Request, post_id):
        article = Article.objects.get(id=post_id)
        article.delete()
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)

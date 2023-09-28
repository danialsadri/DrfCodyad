from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet, ModelViewSet
from .models import Article
from .serializers import UserSerializer, ArticleSerializer, CommentSerializer
from .permissions import BlockListPermission, IsUserOrReadOnly
import requests
from django.shortcuts import get_object_or_404


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
    permission_classes = [BlockListPermission]

    def get(self, request: Request):
        articles = Article.objects.all()
        article_serializer = ArticleSerializer(instance=articles, many=True, context={'request': request})
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
    permission_classes = [IsUserOrReadOnly]

    def put(self, request: Request, post_id):
        article = Article.objects.get(id=post_id)
        self.check_object_permissions(request, article)
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
    permission_classes = [IsUserOrReadOnly]

    def delete(self, request: Request, post_id):
        article = Article.objects.get(id=post_id)
        self.check_object_permissions(request, article)
        article.delete()
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)


class ArticleCommentsView(APIView):
    def get(self, request: Request, article_id):
        comments = Article.objects.get(id=article_id).comments.all()
        comment_serializer = CommentSerializer(instance=comments, many=True)
        return Response(data=comment_serializer.data, status=status.HTTP_200_OK)


class ArticleViewSet(ViewSet):
    def list(self, request: Request):
        queryset = Article.objects.all()
        serializer = ArticleSerializer(instance=queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request):
        serializer = ArticleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request: Request, pk=None):
        queryset = get_object_or_404(Article, id=pk)
        serializer = ArticleSerializer(instance=queryset)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Request, pk=None):
        queryset = get_object_or_404(Article, id=pk)
        serializer = ArticleSerializer(instance=queryset, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request: Request, pk=None):
        queryset = get_object_or_404(Article, id=pk)
        serializer = ArticleSerializer(instance=queryset, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request, pk=None):
        queryset = get_object_or_404(Article, id=pk)
        queryset.delete()
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)


class ArticleModelViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

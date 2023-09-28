from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'home'
router = routers.SimpleRouter()
router.register('viewset', views.ArticleViewSet, 'article_viewset')
router.register('modelviewset', views.ArticleModelViewSet, 'article_modelviewset')
urlpatterns = [
    path('message/', views.MessageView.as_view()),
    path('get_crypto/', views.GetCryptoPrice.as_view()),
    path('user/list/', views.UserListView.as_view()),
    path('article/list/', views.ArticleListView.as_view()),
    path('article/detail/<int:post_id>/', views.ArticleDetailView.as_view()),
    path('article/create/', views.ArticleCreateView.as_view()),
    path('article/update/<int:post_id>/', views.ArticleUpdateView.as_view()),
    path('article/delete/<int:post_id>/', views.ArticleDeleteView.as_view()),
    path('article/comments/<int:article_id>/', views.ArticleCommentsView.as_view()),
    path('article/', include(router.urls)),
]

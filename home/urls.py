from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('message/', views.MessageView.as_view()),
    path('get_crypto/', views.GetCryptoPrice.as_view()),
    path('user/list/', views.UserListView.as_view()),
    path('article/list/', views.ArticleListView.as_view()),
    path('article/detail/<int:post_id>/', views.ArticleDetailView.as_view()),
    path('article/create/', views.ArticleCreateView.as_view()),
    path('article/update/<int:post_id>/', views.ArticleUpdateView.as_view()),
    path('article/delete/<int:post_id>/', views.ArticleDeleteView.as_view()),
]

from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('message/', views.MessageView.as_view()),
    path('get_crypto/', views.GetCryptoPrice.as_view()),
]

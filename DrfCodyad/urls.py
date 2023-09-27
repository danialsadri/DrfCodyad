from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/', include('home.urls', namespace='home')),
    path('api/schema/file/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/login/', obtain_auth_token),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

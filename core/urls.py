from django.contrib import admin
from django.urls import path, include, re_path
from projectmanager_api.views import CustomTokenObtainPairView, CustomTokenRefreshView
from . import settings
from django.conf.urls.static import static 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("projectmanager.urls", namespace="projectmanager")),
    path("api/", include("projectmanager_api.urls", namespace="projectmanager_api")),
    path(
        "api/auth/login", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("api/auth/refresh", CustomTokenRefreshView.as_view(), name="token_refresh"),
    
]

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('projectmanager.urls', namespace="projectmanager")),
    path('api/', include('projectmanager_api.urls', namespace="projectmanager_api")),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

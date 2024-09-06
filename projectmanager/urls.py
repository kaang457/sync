from django.urls import path
from django.views.generic import TemplateView
from .views import dashboard, user_list
from django.conf import settings
from django.conf.urls.static import static

app_name = "projectmanager"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("userlist/", user_list, name="userlist"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

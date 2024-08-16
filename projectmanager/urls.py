from django.urls import path
from django.views.generic import TemplateView
from .views import dashboard, user_list

app_name = "projectmanager"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("userlist/", user_list, name="userlist"),
]

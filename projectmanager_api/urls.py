from django.urls import path, re_path, include
from django.views.generic import TemplateView
from rest_framework import routers
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "projectmanager_api"


urlpatterns = [
    path(
        "clients",
        ClientList.as_view({"get": "list", "post": "create"}),
        name="client_list",
    ),
    path("issues", IssueList.as_view(), name="issue_list"),
    path("issues/<str:id>", issue_detail, name="issue_detail"),
    path("projects", ProjectList.as_view(), name="ProjectList"),
    path("projects/<str:id>", project_detail, name="project_detail"),
    re_path("signup", signup),
    re_path("test_token", test_token),
    path("tasks", TaskList.as_view(), name="tasks"),
    path("tasks/<str:id>", task_detail, name="task_detail"),
    path("subprojects", SubProjectList.as_view(), name="subproject"),
    path("users", UserList.as_view(), name="users"),
    path("users/<str:id>", profile, name="profile"),
    path("tickets", TicketList.as_view(), name="tickets"),
    path("tickets/<str:id>", ticket_detail, name="ticket_detail"),
    path("comments", CommentView.as_view(), name="comments"),
    path("updates", UpdateView.as_view(), name="updates"),
    path("upload/", uploadImage, name="image-upload"),
]

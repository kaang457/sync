from django.urls import path, re_path, include
from django.views.generic import TemplateView
from rest_framework import routers
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "projectmanager_api"

router = routers.DefaultRouter()
router.register(r"clients", ClientList, basename="client")


urlpatterns = [
    path("issues", IssueList, name="issue_list"),
    path("issues/<int:id>", issue_detail, name="issue_detail"),
    path("", include(router.urls)),
    path("projects", ProjectList.as_view(), name="ProjectList"),
    re_path("signup", signup),
    re_path("test_token", test_token),
    path("tasks", TaskList.as_view(), name="tasks"),
    path("subprojects", SubProjectList.as_view(), name="subproject"),
    path("users", UserList.as_view(), name="users"),
    path("users/<int:id>", profile, name="profile"),
    path("tickets", TicketList.as_view(), name="tickets"),
    path("tickets/<int:id>", ticket_detail, name="ticket_detail"),
    path("comments", CommentView.as_view(), name="comments"),
    path("updates", UpdateView.as_view(), name="updates"),
]

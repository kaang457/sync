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
    path("logs", LogList.as_view(), name="listcreate"),
    path("logs/<int:pk>", LogDetail.as_view(), name="detailcreate"),
    path("issues", IssueList.as_view(), name="issuelist"),
    path("issues/<int:id>", IssueRetrieve.as_view(), name="issueretreive"),
    path("", include(router.urls)),
    path("projects", ProjectList.as_view(), name="ProjectList"),
    re_path("signup", signup),
    re_path("test_token", test_token),
    path("checkin", CheckInList.as_view(), name="checkin"),
    path("checkin/<int:pk>", CheckInDetail.as_view(), name="checkindetail"),
    path("subprojects", SubProjectList.as_view(), name="subproject"),
    path("users", UserList.as_view(), name="users"),
    path("tickets", TicketList.as_view(), name="tickets"),
    path("tickets/<int:pk>", TicketUpdate.as_view(), name="ticket-update"),
    path("comments", CommentView.as_view(), name="comments"),
    path("updates", UpdateView.as_view(), name="updates"),
    path("image", ImageView.as_view(), name="images"),
]

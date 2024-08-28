from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics, status, viewsets
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from projectmanager_api.serializers import UserSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from projectmanager.models import (
    Update,
    Comment,
    Image,
    Log,
    Issue,
    Project,
    SubProject,
    Client,
    CheckIn,
    User,
    Ticket,
)
from django.urls import reverse
from .serializers import *
from .forms import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken
from django.utils import timezone
from datetime import timedelta
from django.http import HttpRequest
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.decorators import renderer_classes


class ImageView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class CustomTokenRefreshView(TokenRefreshView):
    def get(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])

        if refresh_token is None:
            return Response(
                {"error": "Refresh token not found"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        fake_request = HttpRequest()
        fake_request.method = "POST"
        fake_request.data = {"refresh": refresh_token}

        response = super().post(fake_request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            new_refresh_token = response.data.get("refresh")
            if new_refresh_token:
                response.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                    value=new_refresh_token,
                    httponly=True,
                    max_age=settings.SIMPLE_JWT[
                        "REFRESH_TOKEN_LIFETIME"
                    ].total_seconds(),
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )
        return response


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            refresh = response.data.get("refresh")
            if refresh:
                response.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                    value=refresh,
                    httponly=True,
                    max_age=settings.SIMPLE_JWT[
                        "REFRESH_TOKEN_LIFETIME"
                    ].total_seconds(),
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )
        return response


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        try:
            user = serializer.save()
            user.set_password(request.data["password"])
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def test_token(request):
    return Response("passed for {}".format(request.user.email))


class LogList(generics.ListCreateAPIView):
    queryset = Log.tasklogobjects.all()
    serializer_class = LogSerializer


class LogDetail(generics.RetrieveUpdateAPIView):
    queryset = Log.tasklogobjects.all()

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return LogUpdateSerializer
        return LogSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        return super().update(request, *args, **kwargs)


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class SubProjectList(generics.ListCreateAPIView):
    queryset = SubProject.objects.all()
    serializer_class = SubProjectSerializer


class UpdateView(generics.ListCreateAPIView):
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(["POST"])
def create_project(request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        if request.user.is_authenticated:
            project = serializer.save(created_by=request.user)
        else:
            return Response(
                {"detail": "Authentication required to create a project."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueList(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


@api_view(["GET", "POST"])
def issue_detail(request, id):
    issue = get_object_or_404(Issue, id=id)

    if request.method == "GET":

        serializer = IssueSerializer(issue)

        return Response(serializer.data)

    elif request.method == "POST":

        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)


class ClientList(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class CheckInList(generics.ListCreateAPIView):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer


class CheckInDetail(generics.RetrieveAPIView):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer


class TicketList(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = BasicTicketSerializer


class TicketUpdate(generics.RetrieveUpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


@api_view(["GET", "PUT"])
def ticket_detail(request, id):
    ticket = get_object_or_404(Ticket, id=id)

    if request.method == "GET":
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

    elif request.method == "PUT":
        data = request.data.copy()
        data["description"] = ticket.description
        data["priority"] = ticket.priority
        data["ticket"] = id
        data["convertFromTicket"] = True

        issue_serializer = IssueSerializer(data=data)

        if issue_serializer.is_valid():
            issue = issue_serializer.save()
            issue.description = ticket.description
            issue.ticket = ticket
            issue.convertedFromTicket = True
            issue.priority = ticket.priority
            issue.save()

            return Response(
                TicketSerializer(issue).data, status=status.HTTP_201_CREATED
            )

        return Response(issue_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

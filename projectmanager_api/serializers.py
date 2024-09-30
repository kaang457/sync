from rest_framework import serializers, status
from projectmanager.models import (
    Update,
    Comment,
    Issue,
    Project,
    SubProject,
    Client,
    User,
    Ticket,
    Task,
)
from datetime import datetime
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist
import uuid


class BasicUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["name", "email", "roles", "id"]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["name", "roles", "email", "password", "id"]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            name=validated_data["name"],
            roles=validated_data["roles"],
            password=validated_data["password"],
        )
        return user


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    created_by = UserSerializer(User, read_only=True)


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = "__all__"


class IssueSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)
    updates = UpdateSerializer(read_only=True, many=True)
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True
    )
    ticket = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.all(), many=False, required=False, allow_null=True
    )
    created_by = UserSerializer(User, read_only=True)

    class Meta:
        model = Issue
        fields = "__all__"

    def to_internal_value(self, data):

        if "ticket" in data and data["ticket"] == "":
            data["ticket"] = None
        return super().to_internal_value(data)

    def to_representation(self, instance):

        representation = super().to_representation(instance)

        representation["assignee"] = BasicUserSerializer(
            instance.assignee, many=True
        ).data

        return representation

    tasks = serializers.SerializerMethodField()

    def get_tasks(self, obj):

        tasks = Task.objects.filter(issue=obj)

        return TaskSerializer(tasks, many=True).data


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class SubProjectSerializer(serializers.ModelSerializer):

    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    projectId = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    createdAt = serializers.DateField(read_only=True)

    class Meta:
        model = SubProject
        fields = "__all__"

    def to_representation(self, instance):

        representation = super().to_representation(instance)

        representation["users"] = BasicUserSerializer(instance.users, many=True).data

        return representation


class ProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    createdAt = serializers.DateField(read_only=True)

    class Meta:
        model = Project
        fields = "__all__"

    sub_projects = serializers.SerializerMethodField()

    def to_representation(self, instance):

        representation = super().to_representation(instance)
        representation["client"] = (
            Client.objects.filter(id=instance.client.id).first().name
        )
        representation["users"] = BasicUserSerializer(instance.users, many=True).data
        representation["owner"] = BasicUserSerializer(instance.owner, many=False).data
        return representation

    def get_sub_projects(self, obj):

        sub_projects = SubProject.objects.filter(projectId=obj)

        return SubProjectSerializer(sub_projects, many=True).data


class BasicTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["description", "content"]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    created_by = UserSerializer(User, read_only=True)

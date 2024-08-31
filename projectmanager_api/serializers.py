from rest_framework import serializers, status
from projectmanager.models import (
    Update,
    Comment,
    Issue,
    Log,
    Project,
    SubProject,
    Client,
    CheckIn,
    User,
    Ticket,
    Image,
    Task,
)
from datetime import datetime
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "name", "roles"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            name=validated_data["name"],
            roles=validated_data["roles"],
        )
        return user


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email"]


class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = "__all__"


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = (
            "id",
            "task",
            "status",
            "is_billable",
            "start_time",
            "end_time",
            "read_only",
            "terminate",
        )
        read_only_fields = ["read_only", "terminate"]


class LogUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = [
            "id",
            "task",
            "status",
            "is_billable",
            "start_time",
            "end_time",
            "total_time",
            "terminate",
        ]
        read_only_fields = (
            "id",
            "task",
            "status",
            "is_billable",
            "start_time",
            "total_time",
            "end_time",
        )

    def update(self, instance, validated_data):
        time_format = "%H:%M:%S.%f"

        if instance.read_only:
            raise serializers.ValidationError(
                "This item is read-only and cannot be modified."
            )

        if "terminate" in validated_data and validated_data["terminate"]:

            instance.read_only = True
            instance.active = False
            instance.terminate = True
            instance.save()
            return instance

        if instance.terminate:
            raise serializers.ValidationError(
                "This item is terminated and cannot be modified."
            )

        if instance.active:
            instance.active = False
            end_time = datetime.now().strftime(time_format)
            start_time = datetime.strptime(str(instance.start_time), time_format)
            end_time = datetime.strptime(end_time, time_format)
            total_time = end_time - start_time
            total_time = total_time.total_seconds()
            instance.total_time += total_time

        elif not instance.active and not instance.terminate:
            instance.active = True
            instance.start_time = datetime.now().strftime(time_format)

        instance = super().update(instance, validated_data)
        instance.save()

        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = "__all__"


class IssueSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(read_only=True)
    update = UpdateSerializer(read_only=True)
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True
    )

    class Meta:
        model = Issue
        fields = "__all__"

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
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    projectId = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    createdAt = serializers.DateField(read_only=True)

    class Meta:
        model = SubProject
        fields = "__all__"

    def to_representation(self, instance):

        representation = super().to_representation(instance)

        representation["users"] = BasicUserSerializer(instance.users, many=True).data
        representation["owner"] = BasicUserSerializer(instance.owner, many=False).data
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
        read_only_fields = ["created_at", "updated_at", "accepted"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

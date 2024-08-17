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
)
from datetime import datetime
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from django.utils.text import slugify


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
    comment = CommentSerializer()
    update = UpdateSerializer()
    assignee = UserSerializer()

    class Meta:
        model = Issue
        fields = "__all__"

    def to_internal_value(self, data):
        if "project" in data and isinstance(data["project"], str):
            try:
                project = Project.objects.get(name=data["project"])
                data["project"] = project.id
            except Project.DoesNotExist:
                raise serializers.ValidationError(
                    {"project": "Project could not be found"}
                )
        if "assignee" in data and isinstance(data["assignee"], str):
            try:
                user = User.objects.get(name=data["assignee"])
                data["assignee"] = user.id
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    {"assignee": "Assignee does not exist"}
                )
        if "comments" not in data:
            data["comments"] = []
        if "updates" not in data:
            data["updates"] = []
        return super().to_internal_value(data)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    sub_project = SubProject

    class Meta:
        model = Project
        fields = "__all__"


class SubProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubProject
        fields = "__all__"

    def to_internal_value(self, data):
        if "users" in data:
            ids = []
            for name in data["users"]:
                try:
                    user = User.objects.get(name=name)
                    ids.append(user.id)
                except ObjectDoesNotExist:
                    continue
            data["users"] = ids
            return super().to_internal_value(data)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"

from django.shortcuts import render
from rest_framework import generics, status
from projectmanager.models import TaskLog, Task, Project
from .serializers import TaskLogSerializer, TaskLogUpdateSerializer, TaskSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, DjangoModelPermissionsOrAnonReadOnly
class TaskLogList(generics.ListCreateAPIView):
    queryset = TaskLog.tasklogobjects.all()
    serializer_class = TaskLogSerializer
    
class TaskLogDetail(generics.RetrieveUpdateAPIView):
    queryset = TaskLog.tasklogobjects.all()
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return TaskLogUpdateSerializer
        return TaskLogSerializer
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        return super().update(request, *args, **kwargs)

class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class=TaskSerializer
    
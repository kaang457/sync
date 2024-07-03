from rest_framework import serializers, status
from projectmanager.models import Task, TaskLog, Project
from datetime import datetime
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from django.utils.text import slugify

class TaskLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskLog
        fields = ('id', 'task', 'status', 'is_billable', 'start_time', 'end_time','read_only', 'terminate')
        read_only_fields = ['read_only', 'terminate']
class TaskLogUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskLog
        fields = ['id', 'task', 'status', 'is_billable', 'start_time', 'end_time', 'total_time', 'terminate']
        read_only_fields = ('id', 'task', 'status', 'is_billable', 'start_time', 'total_time', 'end_time')
        
    def update(self, instance, validated_data):
        time_format = "%H:%M:%S.%f"
        
        if instance.read_only:
            raise serializers.ValidationError("This item is read-only and cannot be modified.")
        
        if 'terminate' in validated_data and validated_data['terminate']:
            
            instance.read_only = True
            instance.active = False
            instance.terminate = True
            instance.save()
            return instance
        
        if instance.terminate:
            raise serializers.ValidationError("This item is terminated and cannot be modified.")
        
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
    
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
    def create(self, validated_data):
        prerequisites = validated_data.pop('prerequisites', [])
        task = Task.objects.create(**validated_data)
        task.prerequisites.set(prerequisites)
        if prerequisites:
            task.status = 'Waiting' 

        return task
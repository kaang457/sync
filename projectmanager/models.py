from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Client(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Project(models.Model):
    name = models.CharField(max_length=100)
    client = models.ForeignKey(
        Client, on_delete=models.PROTECT
    )
    def __str__(self):
        return self.name


class Task(models.Model):    
    options = (
        ('open', 'Open'),
        ('waiting', 'Waiting'),
    )
    project = models.ForeignKey(
        Project, on_delete=models.PROTECT, default = 1
    )
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, null=True)
    description = models.CharField(max_length = 250)
    start_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(
        max_length=10, choices=options, default='open'
    )
   


class TaskLog(models.Model):
    class TaskLogObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='active')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name = 'tasklogs', default = 1
    )
    task = models.ForeignKey(
        Task, on_delete=models.PROTECT, default=1
    )
    options = (
        ('billable', 'Billable'),
        ('non-billable', 'Non-billable'),
    )
    status_choices = (
        ('active', 'Active'),
        ('finished', 'Finished'),
    )
    status=models.CharField(
        max_length=10, choices=status_choices, default='active'
    )
    is_billable=models.CharField(
        max_length=12, choices=options, default='billable'
    )
    start_time = models.TimeField(auto_now_add=True)
    end_time = models.TimeField(auto_now=True)
    total_time = models.FloatField(default=0.0)
    
    
    active = models.BooleanField(default=True)   
    read_only = models.BooleanField(default=False)
    terminate = models.BooleanField(default=False)
    objects = models.Manager()
    tasklogobjects = TaskLogObjects()
    
    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f'TaskLog for {self.task.description} starting at {self.start_time}'

    
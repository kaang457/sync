from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group, Permission, AbstractUser
from .managers import CustomUserManager
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import uuid

MODEL_PREFIX_LENGTH = 3


class BaseModel(models.Model):
    id = models.CharField(
        primary_key=True, max_length=255, editable=True, default=uuid.uuid4
    )
    created_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.id = self.__class__.__name__[:MODEL_PREFIX_LENGTH].upper() + str(self.id)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Image(models.Model):
    image = models.ImageField(upload_to="images/")
    uploaded_at = models.DateTimeField(auto_now=True)


class User(AbstractUser):
    id = models.CharField(
        primary_key=True, max_length=255, editable=True, default=uuid.uuid4
    )

    def save(self, *args, **kwargs):
        self.id = self.__class__.__name__[:MODEL_PREFIX_LENGTH].upper() + str(self.id)
        super().save(*args, **kwargs)

    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("user", "User"),
        ("guest", "Guest"),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    roles = models.CharField(max_length=255, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name

    groups = models.ManyToManyField(
        Group, related_name="projectmanager_user_groups", blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name="projectmanager_user_permissions", blank=True
    )

    REQUIRED_FIELDS = ["name", "roles"]
    USERNAME_FIELD = "email"
    objects = CustomUserManager()


class Client(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(BaseModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_project",
    )
    users = models.ManyToManyField(User)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SubProject(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    users = models.ManyToManyField(User)
    projectId = models.ForeignKey(Project, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")


class Task(BaseModel):
    description = models.CharField(max_length=255)
    issue = models.ForeignKey("Issue", on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    assignee = models.ManyToManyField(User)
    due_date = models.DateField()
    updated_at = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_by", null=True
    )
    man_hour = models.FloatField(default=0.0)
    completed_hour = models.FloatField(default=0.0)
    image = models.ImageField(null=True, blank=True, upload_to="images/")


class Comment(BaseModel):
    content = models.TextField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )


class Update(BaseModel):
    field = models.CharField(max_length=50)
    old_value = models.CharField(max_length=50)
    new_value = models.CharField(max_length=50)


class Ticket(BaseModel):
    description = models.CharField(max_length=255)
    content = models.CharField(max_length=255, default="", blank=True, null=True)
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    TYPE_CHOICES = [
        ("bug", "Bug"),
        ("feature", "Feature"),
        ("question", "Question"),
        ("problem", "Problem"),
    ]
    STATUS_CHOICES = [
        ("open", "open"),
        ("closed", "closed"),
    ]
    accepted = models.BooleanField(default=False)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    comments = models.ManyToManyField(Comment, blank=True)
    updates = models.ManyToManyField(Update, blank=True)


class Issue(BaseModel):
    options = (
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
    )
    labels = [
        ("documentation", "Documentation"),
        ("bug", "Bug"),
        ("feature", "Feature"),
        ("cosmetic", "Cosmetic"),
        ("exception", "Exception"),
    ]
    label = models.CharField(max_length=20, choices=labels, default="task")
    project = models.ForeignKey(Project, on_delete=models.PROTECT)

    priority_options = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    )
    priority = models.CharField(
        max_length=10, choices=priority_options, default="medium"
    )
    project = models.ForeignKey(
        Project, on_delete=models.PROTECT, blank=True, null=True
    )
    subproject = models.ForeignKey(
        SubProject, on_delete=models.CASCADE, null=True, blank=True
    )
    content = models.CharField(max_length=250, blank=True, null=True)
    assignee = models.ManyToManyField(User)
    description = models.CharField(max_length=250)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, blank=True, null=True)
    convertedFromTicket = models.BooleanField(default=False)
    status = models.CharField(max_length=15, choices=options, default="open")
    comments = models.ManyToManyField(Comment, blank=True)
    updated_at = models.DateField(blank=True, null=True)
    updates = models.ManyToManyField(Update, blank=True)

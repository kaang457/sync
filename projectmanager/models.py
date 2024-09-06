from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group, Permission, AbstractUser
from .managers import CustomUserManager
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class User(AbstractUser):
    ROLE_CHOICES = [
        ("Admin", "admin"),
        ("User", "user"),
        ("Guest", "guest"),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    roles = models.CharField(max_length=5, choices=ROLE_CHOICES, default="User")

    groups = models.ManyToManyField(
        Group, related_name="projectmanager_user_groups", blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name="projectmanager_user_permissions", blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "roles"]
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Client(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100)
    createdAt = models.DateField(auto_now=True)
    description = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_project",
    )
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class SubProject(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    users = models.ManyToManyField(User)
    projectId = models.ForeignKey(Project, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    createdAt = models.DateField(auto_now=True)


class Task(models.Model):
    description = models.CharField(max_length=255)
    subproject = models.ForeignKey(
        SubProject, on_delete=models.CASCADE, null=True, blank=True
    )
    issue = models.ForeignKey("Issue", on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    assignee = models.ManyToManyField(User)
    due_date = models.DateField()
    updated_at = models.DateField(blank=True, null=True)
    created_at = models.DateField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_by"
    )
    man_hour = models.FloatField(default=0.0)
    image = models.ImageField(null=True, blank=True, upload_to="images/")


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )


class Update(models.Model):
    field = models.CharField(max_length=50)
    old_value = models.CharField(max_length=50)
    new_value = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)


class Ticket(models.Model):
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
        ("accepted", "accepted"),
        ("waiting", "waiting"),
        ("resolved", "resolved"),
    ]
    accepted = models.BooleanField(default=False)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, blank=True, null=True
    )
    update = models.ForeignKey(Update, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)


class Issue(models.Model):
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
    createdAt = models.DateField(auto_now=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, blank=True, null=True)
    convertedFromTicket = models.BooleanField(default=False)
    status = models.CharField(max_length=15, choices=options, default="open")
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, blank=True, null=True
    )
    updated_at = models.DateField(blank=True, null=True)
    update = models.ForeignKey(Update, on_delete=models.CASCADE, blank=True, null=True)


class Log(models.Model):
    class TaskLogObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status="active")

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasklogs", default=1
    )
    task = models.ForeignKey(Issue, on_delete=models.PROTECT, default=1)
    options = (
        ("billable", "Billable"),
        ("non-billable", "Non-billable"),
    )
    status_choices = (
        ("active", "Active"),
        ("finished", "Finished"),
    )
    status = models.CharField(max_length=10, choices=status_choices, default="active")
    is_billable = models.CharField(max_length=12, choices=options, default="billable")
    start_time = models.TimeField(auto_now_add=True)
    end_time = models.TimeField(auto_now=True)
    total_time = models.FloatField(default=0.0)

    active = models.BooleanField(default=True)
    read_only = models.BooleanField(default=False)
    terminate = models.BooleanField(default=False)
    objects = models.Manager()
    tasklogobjects = TaskLogObjects()

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return f"TaskLog for {self.task.description} starting at {self.start_time}"


class CheckIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="checkin")
    date = models.DateField()
    options = (
        ("Remote", "remote"),
        ("On-site", "on-site"),
    )
    models.CharField(choices=options, max_length=20, default="on-site")

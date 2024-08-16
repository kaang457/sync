# Generated by Django 5.0.6 on 2024-07-05 07:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projectmanager", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="asignee",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 5.0.6 on 2024-06-28 09:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("projectmanager", "0009_alter_tasklog_total_time"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tasklog",
            name="task",
        ),
        migrations.RemoveField(
            model_name="tasklog",
            name="user",
        ),
    ]

# Generated by Django 5.0.6 on 2024-07-14 21:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("projectmanager", "0005_project_prerequisites_task_assignee"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="team",
            name="players",
        ),
        migrations.DeleteModel(
            name="Player",
        ),
        migrations.DeleteModel(
            name="Team",
        ),
    ]

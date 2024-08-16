# Generated by Django 5.0.6 on 2024-08-06 09:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0017_alter_user_managers_alter_user_roles'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='feature',
            new_name='label',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='created_by',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='assignee',
            new_name='users',
        ),
        migrations.RemoveField(
            model_name='project',
            name='start_date',
        ),
        migrations.AddField(
            model_name='project',
            name='created_at',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.CharField(default='x', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='issue',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='priority',
            field=models.CharField(choices=[('low', 'Low'), ('Medium', 'medium'), ('High', 'high'), ('Critical', 'critical')], default='medium', max_length=10),
        ),
        migrations.AlterField(
            model_name='issue',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='project',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]

# Generated by Django 5.0.6 on 2024-08-08 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0025_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='description',
            field=models.CharField(default='x', max_length=255),
            preserve_default=False,
        ),
    ]

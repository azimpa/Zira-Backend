# Generated by Django 5.0.1 on 2024-02-25 09:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("instructor", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="course",
            name="category",
        ),
        migrations.RemoveField(
            model_name="course",
            name="image",
        ),
        migrations.RemoveField(
            model_name="course",
            name="video_url",
        ),
    ]

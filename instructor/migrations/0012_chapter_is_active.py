# Generated by Django 5.0.1 on 2024-04-24 19:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("instructor", "0011_rename_course_status_course_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="chapter",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]

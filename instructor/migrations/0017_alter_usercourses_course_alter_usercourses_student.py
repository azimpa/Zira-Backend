# Generated by Django 5.0.1 on 2024-05-24 12:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("instructor", "0016_remove_usercourses_courses_usercourses_course_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="usercourses",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="students_enrolled",
                to="instructor.course",
            ),
        ),
        migrations.AlterField(
            model_name="usercourses",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
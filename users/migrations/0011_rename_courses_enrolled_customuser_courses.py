# Generated by Django 4.2.2 on 2024-05-23 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_customuser_course_customuser_courses_enrolled'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='courses_enrolled',
            new_name='courses',
        ),
    ]

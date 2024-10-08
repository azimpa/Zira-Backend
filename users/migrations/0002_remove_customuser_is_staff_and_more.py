# Generated by Django 5.0.1 on 2024-01-28 11:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="is_staff",
        ),
        migrations.AlterField(
            model_name="customuser",
            name="contact_number",
            field=models.CharField(max_length=13, unique=True),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="experience",
            field=models.IntegerField(default=0),
        ),
    ]
# Generated by Django 5.0.1 on 2024-03-19 16:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("adminzira", "0003_category_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="category/"),
        ),
    ]
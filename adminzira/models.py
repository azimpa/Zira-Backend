from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
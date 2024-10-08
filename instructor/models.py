from django.db import models
from adminzira.models import Category
from users.models import CustomUser
from django.core.validators import FileExtensionValidator


class Course(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    duration = models.DurationField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    language = models.CharField(max_length=50,choices=[('english', 'English'), ('malayalam', 'Malayalam'), ('tamil', 'Tamil'),])
    level = models.CharField(max_length=20, choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced'),])
    image = models.ImageField(upload_to="courses/images/", blank=True, null=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    status = models.CharField(max_length=30, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'),], default='Pending') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    content = models.TextField()
    duration = models.DurationField(blank=True, null=True)
    image = models.ImageField(upload_to="courses/images/", blank=True, null=True)
    video = models.FileField(upload_to="courses/videos/", validators=[FileExtensionValidator(['mp4', 'avi', 'mkv'])], blank=True, null=True)
    preview_video = models.FileField(upload_to="courses/videos/", validators=[FileExtensionValidator(['mp4', 'avi', 'mkv'])], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    

class UserCourses(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students_enrolled')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


# completion_status = models.CharField(max_length=20, choices=[('incomplete', 'Incomplete'), ('complete', 'Complete')], default='incomplete')
# grade = models.FloatField(null=True, blank=True)
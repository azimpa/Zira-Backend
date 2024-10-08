from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        

class AdminDashboardSerializer(serializers.Serializer):
    class CourseStatsDataSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=200)
        student_count = serializers.IntegerField()

    weekly_sales = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_students_count = serializers.IntegerField()
    total_sales = serializers.DecimalField(max_digits=10, decimal_places=2)
    course_purchase_data = serializers.ListField(child=serializers.IntegerField(), min_length=12, max_length=12)
    course_stats_data = CourseStatsDataSerializer(many=True)
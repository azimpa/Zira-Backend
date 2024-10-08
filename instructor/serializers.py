from rest_framework import serializers
from .models import Course, Chapter, UserCourses

# from adminzira.serializers import CategorySerializer
# from users.serializers import UserSerializer


class CourseSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()
    # instructor = UserSerializer()

    class Meta:
        model = Course
        fields = "__all__"


class ChapterSerializer(serializers.ModelSerializer):
    # course = CourseSerializer()
    class Meta:
        model = Chapter
        fields = "__all__"


class UserCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourses
        fields = "__all__"


class InstructorDashboardSerializer(serializers.Serializer):
    class CourseStatsDataSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=200)
        student_count = serializers.IntegerField()

    total_sales = serializers.DecimalField(max_digits=10, decimal_places=2)
    student_count = serializers.IntegerField()
    completion_rate = serializers.IntegerField()
    course_purchase_data = serializers.ListField(
        child=serializers.IntegerField(), min_length=12, max_length=12
    )
    course_stats_data = CourseStatsDataSerializer(many=True)

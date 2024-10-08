from rest_framework import generics, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Course, Chapter, UserCourses
from .serializers import (
    CourseSerializer,
    ChapterSerializer,
    InstructorDashboardSerializer,
    UserCoursesSerializer,
)
from payment.models import PaymentDetails
from django.db.models import Count
from django.db.models.functions import ExtractMonth


class CourseListCreateEdit(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # permission_classes = [IsAuthenticated]


class InstructorCourseList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer

    def get_queryset(self):
        ins_id = self.kwargs["pk"]
        queryset = Course.objects.filter(instructor=ins_id)
        return queryset


class CourseRetrieveUpdate(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = not instance.is_active
        instance.save()
        status_text = "Blocked" if instance.is_active else "Unblocked"
        serializer = self.get_serializer(instance)
        return Response(
            {
                "detail": f"Course {status_text.lower()} successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ChapterListCreateEdit(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer


class ChapterRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = not instance.is_active
        instance.save()
        status_text = "Blocked" if instance.is_active else "Unblocked"
        serializer = self.get_serializer(instance)
        return Response(
            {
                "detail": f"Course {status_text.lower()} successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class InstructorDashboardView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = InstructorDashboardSerializer

    def get(self, request):
        instructor = request.user
        courses = Course.objects.filter(instructor=instructor)
        payments = PaymentDetails.objects.filter(course__in=courses)

        course_purchase_data = (
            payments.annotate(month=ExtractMonth("date"))
            .values("month")
            .annotate(purchase_count=Count("id"))
        )

        course_purchase_counts = [0] * 12
        for entry in course_purchase_data:
            course_purchase_counts[entry["month"] - 1] = entry["purchase_count"]

        course_stats_data = (
            Course.objects.filter(instructor=instructor)
            .values("title")
            .annotate(student_count=Count("payments__user", distinct=True))
        )

        total_sales = sum(payment.price for payment in payments)
        student_count = len(set(payment.user for payment in payments))
        completion_rate = 90  # Placeholder for actual completion rate calculation

        data = {
            "total_sales": total_sales,
            "student_count": student_count,
            "completion_rate": completion_rate,
            "course_purchase_data": course_purchase_counts,
            "course_stats_data": list(course_stats_data),
        }

        serializer = self.serializer_class(data)
        return Response(serializer.data)


class UserCoursesListView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = UserCourses.objects.all()
    serializer_class = UserCoursesSerializer


class UserCoursesRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserCourses.objects.all()
    serializer_class = UserCoursesSerializer

    def get_object(self):
        student_id = self.kwargs.get("student_id")
        course_id = self.kwargs.get("course_id")
        return UserCourses.objects.get(student_id=student_id, course_id=course_id)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = not instance.is_active
        instance.save()
        status_text = "unblocked" if instance.is_active else "blocked"
        serializer = self.get_serializer(instance)
        return Response(
            {
                "detail": f"Enrollment {status_text} successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

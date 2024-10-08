from rest_framework import generics, status
from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Category
from rest_framework.views import APIView
from .serializers import CategorySerializer, AdminDashboardSerializer
from payment.models import PaymentDetails
from users.models import CustomUser
from users.serializers import UserSerializer
from instructor.models import Course
from instructor.serializers import CourseSerializer
from django.db.models import Count, Sum
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from datetime import timedelta
# from rest_framework.permissions import IsAuthenticated
# from zira_project.permissions import IsAdminOrInstructor


class UserListView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.exclude(Q(is_superuser=True) | Q(is_instructor=True))
    serializer_class = UserSerializer


class ToggleUserStatus(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = not instance.is_active
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class InstructorListView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.filter(is_instructor=True)
    serializer_class = UserSerializer


class ToggleInstructorStatus(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_approved = not instance.is_approved
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryListCreateEdit(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated, IsAdminOrInstructor]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated, IsAdminOrInstructor]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ToggleCategoryStatus(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = not instance.is_active
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
class CourseRetrieveUpdateStatus(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        new_status = request.data.get("status")
        if new_status in ["Approved", "Rejected"]:
            instance.status = new_status
            instance.save()
            serializer = self.get_serializer(instance)
            return Response({"detail": f"Course {new_status.lower()}ed successfully", "data": serializer.data}, status=status.HTTP_200_OK,)
        return Response({"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = not instance.is_active
        instance.save()
        status_text = "Blocked" if instance.is_active else "Unblocked"
        serializer = self.get_serializer(instance)
        return Response({"detail": f"Course {status_text.lower()} successfully", "data": serializer.data}, status=status.HTTP_200_OK,)
    
    
class AdminDashboardView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = AdminDashboardSerializer

    def get(self, request):
        course_purchase_data = PaymentDetails.objects.annotate(month=ExtractMonth('date')).values('month').annotate(purchase_count=Count('id'))
        course_purchase_counts = [0] * 12
        for entry in course_purchase_data:
            course_purchase_counts[entry['month'] - 1] = entry['purchase_count']
            
        course_stats_data = Course.objects.values('title').annotate(student_count=Count('payments__user', distinct=True))
        
        total_sales = PaymentDetails.objects.aggregate(total=Sum('price'))['total']

        student_count = PaymentDetails.objects.values('user').distinct().count()

        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())  # weekday() returns 0 for Monday, 1 for Tuesday, ..., 6 for Sunday
        weekly_sales = PaymentDetails.objects.filter(date__gte=week_start).aggregate(total=Sum('price'))['total']

        data = {
            "weekly_sales": weekly_sales or 0,
            "total_students_count": student_count or 0,
            "total_sales": total_sales or 0,
            "course_purchase_data": course_purchase_counts,
            "course_stats_data": list(course_stats_data),
        }

        serializer = self.serializer_class(data)
        return Response(serializer.data)  
from django.urls import path
from . import views

urlpatterns = [
    path("userlist", views.UserListView.as_view(), name="user-list"),
    path("userstatus/<int:pk>/", views.ToggleUserStatus.as_view(), name="user-status"),
    path("instructorlist", views.InstructorListView.as_view(), name="instructor-list"),
    path("instructorstatus/<int:pk>/", views.ToggleInstructorStatus.as_view(), name="instructor-status"),
    path("category", views.CategoryListCreateEdit.as_view(), name="category-list"),
    path("category/<int:pk>/", views.CategoryRetrieveUpdateDeleteView.as_view(), name="category-retrieve-update-delete"),
    path("categorystatus/<int:pk>/", views.ToggleCategoryStatus.as_view(), name="category-status"),
    path("course/<int:pk>/", views.CourseRetrieveUpdateStatus.as_view(), name="course-retrieve-update-status"),
    path('admin-dashboard', views.AdminDashboardView.as_view(), name='admin-dashboard'),
]
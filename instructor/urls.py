from django.urls import path
from . import views

urlpatterns = [
    path("course", views.CourseListCreateEdit.as_view(), name="course-list-create"),
    path("course/<int:pk>/", views.CourseRetrieveUpdate.as_view(), name="course-retrieve-update"),
    path("chapter", views.ChapterListCreateEdit.as_view(), name="chapter-list-create"),
    path("chapter/<int:pk>/", views.ChapterRetrieveUpdateDeleteView.as_view(), name="chapter-retrieve-update-delete"),
    path("instructor-course/<int:pk>/", views.InstructorCourseList.as_view(), name="instructor-course"),
    path('instructor-dashboard', views.InstructorDashboardView.as_view(), name='instructor-dashboard'),
    path('user-courses', views.UserCoursesListView.as_view(), name='user-courses'),
    path('enrollment/<int:student_id>/<int:course_id>/', views.UserCoursesRetrieveUpdateDeleteView.as_view(), name='enrollment'),
]
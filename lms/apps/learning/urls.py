from django.urls import path
from .views import Register, Verify, CourseDetail, AllCourses, CourseEnrollment

urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("verify/", Verify.as_view(), name="verify"),
    path("courses/<int:course_id>/", CourseDetail.as_view(), name="course-detail"),
    # Following views require authentication
    path("all_courses/", AllCourses.as_view(), name="all-courses"),
    path("course_enrollment/", CourseEnrollment.as_view(), name="course-enrollment"),
]

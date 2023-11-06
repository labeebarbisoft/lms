from django.urls import path
from .views import (
    Register,
    Verify,
    CourseDetail,
    AllCourses,
    CourseEnrollment,
    QueryCounteTest,
)

urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("verify/", Verify.as_view(), name="verify"),
    path("courses/<int:course_id>/", CourseDetail.as_view(), name="course-detail"),
    # Following views require authentication
    path("all_courses/", AllCourses.as_view(), name="all-courses"),
    path("course_enrollment/", CourseEnrollment.as_view(), name="course-enrollment"),
    # Following views are for testing only
    path("query_count/", QueryCounteTest.as_view(), name="query_count"),
]

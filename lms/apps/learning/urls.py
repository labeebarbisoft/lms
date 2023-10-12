from django.urls import path
from .views import Register, Verify, CourseDetail

urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("verify/", Verify.as_view(), name="verify"),
    path("courses/<int:course_id>/", CourseDetail.as_view(), name="course-detail"),
]

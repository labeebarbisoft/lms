from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, EmailAndOtpSerializer, EnrollStudentSerializer
from lms.apps.studio.serializers import CourseSerializer, CourseOverviewSerializer
from lms.apps.studio.models import Course, Profile
from rest_framework.permissions import IsAuthenticated
from .permissions import IsUserVerified, IsUserStudent


class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class Verify(APIView):
    def post(self, request):
        serializer = EmailAndOtpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            otp = serializer.data.get("otp")
            user = User.objects.filter(email=email).first()
            if (
                user is not None
                and Profile.objects.verify_user(user.profile, otp) is True
            ):
                return Response(
                    {"message": "Verified successfully."}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "Invalid email or otp."},
                    status=status.HTTP_400_BAD_REQUEST,
                )


class CourseDetail(APIView):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
            serializer = CourseSerializer(course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response(
                {"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND
            )


class AllCourses(APIView):
    permission_classes = [IsAuthenticated, IsUserVerified, IsUserStudent]

    def post(self, request):
        enrolled_courses_serializer = CourseOverviewSerializer(
            Profile.objects.get_enrolled_courses(request.profile), many=True
        )
        available_courses_serializer = CourseOverviewSerializer(
            Profile.objects.get_available_courses(request.profile), many=True
        )
        response_data = {
            "enrolled_courses": enrolled_courses_serializer.data,
            "available_courses": available_courses_serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class CourseEnrollment(APIView):
    permission_classes = [IsAuthenticated, IsUserVerified, IsUserStudent]

    def post(self, request):
        serializer = EnrollStudentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            course_ids = serializer.validated_data.get("course_ids", [])
            Profile.objects.add_courses(request.profile, course_ids)
            return Response(
                {"message": "Enrollment successful"}, status=status.HTTP_200_OK
            )


class QueryCounteTest(APIView):
    def get(self, request):
        return Response(
            {
                "username": request.user.username,
                "profile otp": request.profile.otp,
            },
            status=status.HTTP_200_OK,
        )

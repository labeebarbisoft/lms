from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, EmailAndOtpSerializer
from lms.apps.studio.serializers import CourseSerializer
from lms.apps.studio.models import Course
from .tasks import send_email_task


class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.profile.role = "student"
            user.profile.is_verified = False
            user.profile.save()
            # send_email_task.delay(
            #     "OTP", str(user.profile.otp), "muhammad.labeeb@gmail.com", [user.email]
            # )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Verify(APIView):
    def post(self, request):
        serializer = EmailAndOtpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            otp = serializer.data.get("otp")
            user = User.objects.filter(email=email).first()
            if user and user.profile.otp == otp:
                user.profile.is_verified = True
                user.profile.save()
                return Response(
                    {"message": "Verified successfully."}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "Invalid email or otp."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

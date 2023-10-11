from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, EmailAndOtpSerializer


class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.profile.role = "student"
            user.profile.is_verified = False
            user.profile.save()
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

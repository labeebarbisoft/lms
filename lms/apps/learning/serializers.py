from rest_framework import serializers
from django.contrib.auth.models import User
from .models import EmailAndOtp


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]


class EmailAndOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAndOtp
        fields = ["email", "otp"]

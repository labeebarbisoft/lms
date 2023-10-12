from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]


class EmailAndOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()


class EnrollStudentSerializer(serializers.Serializer):
    course_ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )

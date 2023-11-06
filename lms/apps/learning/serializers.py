from rest_framework import serializers
from django.contrib.auth.models import User
from .tasks import send_email_task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.role = "student"
        user.save()
        # send_email_task.delay(
        #     "OTP", str(user.profile.otp), "muhammad.labeeb@gmail.com", [user.email]
        # )
        return user


class EmailAndOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()


class EnrollStudentSerializer(serializers.Serializer):
    course_ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )

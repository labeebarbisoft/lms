import random
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def generate_random_otp():
    return random.randint(100000, 999999)


class Course(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, related_name="courses", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class ProfileManager(models.Manager):
    def verify_user(self, profile, otp):
        if profile.otp == otp:
            profile.is_verified = True
            profile.save()
        return profile.is_verified

    def add_courses(self, profile, course_ids):
        courses = Course.objects.filter(id__in=course_ids)
        profile.courses.add(*courses)

    def get_enrolled_courses(self, profile):
        return profile.courses.all()

    def get_available_courses(self, profile):
        all_courses = Course.objects.all()
        enrolled_courses = self.get_enrolled_courses(profile)
        available_courses = [
            course for course in all_courses if course not in enrolled_courses
        ]
        return available_courses


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_TYPES = [
        ("student", "Student"),
        ("author", "Author"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_TYPES)
    otp = models.PositiveIntegerField(default=generate_random_otp)
    is_verified = models.BooleanField(default=True)
    courses = models.ManyToManyField(Course, related_name="profiles")

    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, role="author")


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Section(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(
        Course, related_name="sections", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name}"


class SubSection(models.Model):
    name = models.CharField(max_length=100)
    section = models.ForeignKey(
        Section, related_name="subsections", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name}"


class Unit(models.Model):
    name = models.CharField(max_length=100)
    sub_section = models.ForeignKey(
        SubSection, related_name="units", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name}"


class Component(models.Model):
    name = models.CharField(max_length=100)
    content = models.CharField(max_length=10000)
    unit = models.ForeignKey(Unit, related_name="components", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

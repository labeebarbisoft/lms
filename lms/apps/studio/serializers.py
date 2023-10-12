from rest_framework import serializers
from .models import Course, Section, SubSection, Unit, Component


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ["name", "content"]


class UnitSerializer(serializers.ModelSerializer):
    components = ComponentSerializer(many=True)

    class Meta:
        model = Unit
        fields = ["name", "components"]


class SubSectionSerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True)

    class Meta:
        model = SubSection
        fields = ["name", "units"]


class SectionSerializer(serializers.ModelSerializer):
    subsections = SubSectionSerializer(many=True)

    class Meta:
        model = Section
        fields = ["name", "subsections"]


class CourseSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source="author.username", read_only=True, required=False
    )
    sections = SectionSerializer(many=True)

    class Meta:
        model = Course
        fields = ["name", "author_name", "sections"]


class CourseOverviewSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source="author.username", read_only=True, required=False
    )

    class Meta:
        model = Course
        fields = ["id", "name", "author_name"]

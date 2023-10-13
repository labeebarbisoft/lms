from django.contrib import admin
from .models import Profile, Course, Section, SubSection, Unit, Component


@admin.register(Course)
class Course(admin.ModelAdmin):
    list_display = ("name", "author", "enrolled_students_count")
    list_filter = ("author",)

    def enrolled_students_count(self, obj):
        return obj.profiles.count()

    enrolled_students_count.short_description = "Enrolled Students"


@admin.register(Profile)
class Course(admin.ModelAdmin):
    list_display = ("user", "role", "get_user_is_verified")
    list_filter = ("role", "is_verified")

    @admin.display(boolean=True)
    def get_user_is_verified(self, obj):
        return obj.is_verified

    get_user_is_verified.short_description = "Is Verified"


@admin.register(Section)
class Section(admin.ModelAdmin):
    list_display = ("name", "course")
    list_filter = ("course",)


@admin.register(SubSection)
class SubSection(admin.ModelAdmin):
    list_display = ("name", "section", "course_name")
    list_filter = ("section", "section__course")

    def course_name(self, obj):
        return obj.section.course.name

    course_name.short_description = "Course Name"


@admin.register(Unit)
class Unit(admin.ModelAdmin):
    list_display = ("name", "sub_section", "section_name", "course_name")
    list_filter = (
        "sub_section",
        "sub_section__section",
        "sub_section__section__course",
    )

    def section_name(self, obj):
        return obj.sub_section.section.name

    section_name.short_description = "Section"

    def course_name(self, obj):
        return obj.sub_section.section.course.name

    course_name.short_description = "Course"


@admin.register(Component)
class Component(admin.ModelAdmin):
    list_display = ("name", "unit", "course_name")
    list_filter = (
        "unit",
        "unit__sub_section",
        "unit__sub_section__section",
        "unit__sub_section__section__course",
    )

    def course_name(self, obj):
        return obj.unit.sub_section.section.course.name

    course_name.short_description = "Course"

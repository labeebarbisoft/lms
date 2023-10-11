from django.contrib import admin
from .models import Profile, Course, Section, SubSection, Unit, Component


admin.site.register(Profile)
admin.site.register(Section)
admin.site.register(SubSection)
admin.site.register(Unit)


@admin.register(Component)
class Component(admin.ModelAdmin):
    list_display = ("name", "unit")


@admin.register(Course)
class Course(admin.ModelAdmin):
    list_display = ("name", "author")
    list_filter = ("author",)

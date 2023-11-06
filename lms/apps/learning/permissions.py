from rest_framework import permissions


class IsUserVerified(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.profile.is_verified


class IsUserStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        # return True
        return request.profile.role == "student"

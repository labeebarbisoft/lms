from django.utils.functional import SimpleLazyObject
from .models import Profile
import logging


# class ProfileMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         request.profile = SimpleLazyObject(lambda: self.get_profile(request))
#         response = self.get_response(request)
#         return response

#     def get_profile(self, request):
#         if not request.user.is_anonymous:
#             return Profile.objects.get(user=request.user)
#         return None

from django.urls import path
from .views import Register, Verify

urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("verify/", Verify.as_view(), name="verify"),
]

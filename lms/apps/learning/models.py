from django.db import models


class EmailAndOtp(models.Model):
    email = models.CharField(max_length=100)
    otp = models.IntegerField()

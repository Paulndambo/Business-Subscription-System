from django.db import models
from django.contrib.auth.models import AbstractUser

from core.models import AbstractBaseModel

# Create your models here.
GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
)

USER_ROLES = (
    ("Admin", "Admin"),
    ("Customer", "Customer"),
    ("Business Owner", "Business Owner"),
)


class User(AbstractUser, AbstractBaseModel):
    role = models.CharField(max_length=255, choices=USER_ROLES)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    postal_code = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.username

    def name(self):
        return f"{self.first_name} {self.last_name}"

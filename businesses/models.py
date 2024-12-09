from django.db import models

from core.models import AbstractBaseModel


# Create your models here.
class Business(AbstractBaseModel):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    subscription_package = models.ForeignKey("payments.SubscriptionPackage", on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BusinessBranch(AbstractBaseModel):
    name = models.CharField(max_length=255)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="branches")
    subscription_package = models.ForeignKey("payments.SubscriptionPackage", on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

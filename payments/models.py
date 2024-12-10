from django.db import models

from core.models import AbstractBaseModel

PAYMENT_STATUSES = (
    ("Pending", "Pending"),
    ("Complete", "Complete"),
    ("Cancelled", "Cancelled"),
    ("Future", "Future"),
    ("Failed", "Failed"),
    ("Incomplete", "Incomplete"),
)


CURRENCY_CHOICES = (
    ("KES", "KES"),
    ("USD", "USD"),
)

SUBSCRIPTION_TYPES = (
    ("Business Subscription", "Business Subscription"),
    ("Branch Subscription", "Branch Subscription"),
)


# Create your models here.
class SubscriptionPackage(AbstractBaseModel):
    name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    max_products = models.IntegerField(default=10)
    unlimited_products = models.BooleanField(default=False)
    plan_code = models.CharField(max_length=255, null=True)
    interval = models.CharField(max_length=255, null=True)
    send_invoices = models.BooleanField(default=True)
    send_sms = models.BooleanField(default=True)
    hosted_page = models.BooleanField(default=True)
    currency = models.CharField(max_length=255, default="KES", choices=CURRENCY_CHOICES)
    subscription_page = models.UUIDField(null=True)

    def __str__(self):
        return self.name


class Subscription(AbstractBaseModel):
    business = models.ForeignKey(
        "businesses.Business", on_delete=models.CASCADE, null=True
    )
    business_branch = models.ForeignKey(
        "businesses.BusinessBranch", on_delete=models.SET_NULL, null=True
    )
    subscription_package = models.ForeignKey(
        SubscriptionPackage, on_delete=models.SET_NULL, null=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    active = models.BooleanField(default=False)
    payment_link = models.URLField(null=True)
    subscription_type = models.CharField(
        max_length=255, choices=SUBSCRIPTION_TYPES, default="Business Subscription"
    )

    def __str__(self):
        return self.business.name


class SubscriptionPayment(AbstractBaseModel):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    payment_reference = models.CharField(max_length=255, null=True)
    payer = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    amount_expected = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_expected = models.DateField(null=True)
    payment_status = models.CharField(
        max_length=255, choices=PAYMENT_STATUSES, default="Pending"
    )
    payment_link = models.URLField(null=True)

    def __str__(self):
        return self.payer.username

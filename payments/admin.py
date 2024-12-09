from django.contrib import admin

from payments.models import SubscriptionPackage, Subscription, SubscriptionPayment
# Register your models here.
@admin.register(SubscriptionPackage)
class SubscriptionPackageAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "cost", "max_products", "unlimited_products"]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["id", "business", "business_branch", "amount", "subscription_type"]


@admin.register(SubscriptionPayment)
class SubscriptionPaymentAdmin(admin.ModelAdmin):
    list_display = ["id", "subscription", "payment_reference", "amount_expected", "amount_paid", "payment_status"]
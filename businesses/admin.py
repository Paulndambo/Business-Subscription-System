from django.contrib import admin

from businesses.models import Business, BusinessBranch
# Register your models here.
@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "owner", "subscription_package", "active"]


@admin.register(BusinessBranch)
class BusinessBranchAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "business", "subscription_package", "active"]


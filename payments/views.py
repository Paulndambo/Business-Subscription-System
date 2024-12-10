from django.shortcuts import render
from django.conf import settings
from django.db import transaction

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from core.permissions import IsBusinessOwner

from payments.models import SubscriptionPackage, Subscription, SubscriptionPayment
from payments.serializers import (
    SubscriptionPackageSerializer,
    SubscriptionSerializer,
    SubscriptionPaymentSerializer,
    BusinessSubscriptionSerializer,
)

from businesses.models import Business
from core.paystack import PaystackInterface

# Create your views here.
"""Subscription Packages
Subscription packages can only be created, edit and deleted by admins,
While Business Owners can only view them.

Subscription Packages Include:
    1. Starter.
    2. Premium.
    3. Pro.
    4. BranchPlan (This is used to bill businesses for branches created)
"""


class SubscriptionPackageListCreateAPIView(generics.ListCreateAPIView):
    queryset = SubscriptionPackage.objects.all()
    serializer_class = SubscriptionPackageSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            name = serializer.validated_data.get("name")
            max_products = serializer.validated_data.get("max_products")
            unlimited_products = serializer.validated_data.get("unlimited_products")
            cost = serializer.validated_data.get("cost")
            interval = serializer.validated_data.get("interval").lower()
            currency = serializer.validated_data.get("currency")

            paystack = PaystackInterface()
            x = paystack.create_plan(
                name=name, amount=int(cost), interval=interval, currency=currency
            )
            print(x)
            plan_code = x["plan_code"]

            SubscriptionPackage.objects.create(
                name=name,
                max_products=max_products,
                unlimited_products=unlimited_products,
                cost=cost,
                plan_code=plan_code,
                currency=currency,
                interval=interval,
            )
            return Response({"success": "You have successfully subscribed"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionPackageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubscriptionPackage.objects.all()
    serializer_class = SubscriptionPackageSerializer

    lookup_field = "pk"


"""Subscriptions
Subscriptions belong to business owners, based on the subscription package subscribed on,
The business owner is able to know how many products he/she can list.
"""


class SubscriptionAPIView(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class SubscriptionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    lookup_field = "pk"


class SubscribeAPIView(generics.CreateAPIView):
    serializer_class = BusinessSubscriptionSerializer
    permission_classes = [IsAuthenticated, IsBusinessOwner]

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            business_id = serializer.validated_data.get("business")
            package_id = serializer.validated_data.get("subscription_package")

            business = Business.objects.get(id=business_id)
            package = SubscriptionPackage.objects.get(id=package_id)

            business.subscription_package = package
            business.save()

            subscription = Subscription.objects.create(
                business=business,
                subscription_package=package,
                amount=package.cost,
                subscription_type="Business Subscription",
            )

            return Response(
                {"success": "Subscribed successfully!!"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


""" Subscripion Payments
Subscription payments are just payment records, for audit and security purposes, these records
cannot be edit or deleted.

They are created and updated on the background by cronjobs/scheduled tasks.

They are available to;-
    1. Subscription owners. 
    2. Platform admins.
"""


class SubscriptionPaymentAPIView(generics.ListAPIView):
    queryset = SubscriptionPayment.objects.all().order_by("-created_on")
    serializer_class = SubscriptionPaymentSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(payer=user)


class SubscriptionPaymentDetailAPIView(generics.RetrieveAPIView):
    queryset = SubscriptionPayment.objects.all().order_by("-created_on")
    serializer_class = SubscriptionPaymentSerializer

    permission_classes = [IsAuthenticated]

    lookup_field = "pk"


class PaystackCallbackAPIView(APIView):
    def get(self, request):
        return Response({"success": "Payment processed successfully!!"})

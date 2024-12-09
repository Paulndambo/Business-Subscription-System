from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from payments.models import SubscriptionPackage, Subscription, SubscriptionPayment
from payments.serializers import (
    SubscriptionPackageSerializer,
    SubscriptionSerializer,
    SubscriptionPaymentSerializer,
    BusinessSubscriptionSerializer
)


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


class SubscriptionPackageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubscriptionPackage.objects.all()
    serializer_class = SubscriptionPackageSerializer

    lookup_field = "pk"


"""Subscriptions
Subscriptions belong to business owners, based on the subscription package subscribed on,
The business owner is able to know how many products he/she can list.
"""

class SubscriptionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]


    def get_serializer_class(self):
        if self.request.method == "POST":
            return BusinessSubscriptionSerializer
        return SubscriptionSerializer

    
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    lookup_field = "pk"


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

        if request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(payer=user)


class SubscriptionPaymentDetailAPIView(generics.RetrieveAPIView):
    queryset = SubscriptionPayment.objects.all().order_by("-created_on")
    serializer_class = SubscriptionPaymentSerializer

    permission_classes = [IsAuthenticated]

    lookup_field = "pk"


class PaystackCallbackAPIView(APIView):
    def get(self, request):
        return Response({ "success": "Payment processed successfully!!" })
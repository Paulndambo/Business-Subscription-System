from django.shortcuts import render
from django.db import transaction

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from businesses.models import Business, BusinessBranch
from businesses.serializers import BusinessSerializer, BusinessBranchSerializer

from payments.models import SubscriptionPayment

from payments.models import Subscription
from businesses.permissions import IsBusinessOwner

from payments.generate_payment_links import generate_payment_link

# Create your views here.
class BusinessListAPIView(generics.ListCreateAPIView):
    """
    This view is for creating and listing businesses.
    However, only business owners can create, customers can just view.
    """
    queryset = Business.objects.all().order_by("-created_on")
    serializer_class = BusinessSerializer


    def get_permissions(self):
        """Security Check:
            Only someone who is logged and is a business owner can create a business.
        """
        if self.request.method == "POST":
            return [IsAuthenticated(), IsBusinessOwner()]
        return [AllowAny()]


    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):

            link = generate_payment_link(12, user.email, 20)
            print(link)

            """
            business = serializer.save()
            business.owner = user
            business.save()

            """
            #When Creating a business, a subscription is also created.
            """
            subscription = Subscription.objects.create(
                business=business,
                subscription_package=business.subscription_package,
                amount=business.subscription_package.cost,
            )
            payment = SubscriptionPayment.objects.create(
                subscription=subscription,
                payer=business.owner,
                amount_expected=subscription.amount
            )

            """
            return Response(
                {"success": "Business Created Successfully!!"},
                status=status.HTTP_201_CREATED,
            )
            
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Business.objects.all().order_by("-created_on")
    serializer_class = BusinessSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "OPTIONS", "DELETE"]:
            return [IsAuthenticated(), IsBusinessOwner()]
        return [AllowAny()]


class BusinessBranchAPIView(generics.ListCreateAPIView):
    queryset = BusinessBranch.objects.all().order_by("-created_on")
    serializer_class = BusinessBranchSerializer

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsBusinessOwner()]
        return [AllowAny()]


    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            branch = serializer.save()

            package = SubscriptionPackage.objects.filter(subscription_type="Branch Plan").first()

            if not package:
                package = SubscriptionPackage.objects.create(
                    name="Branch Plan",
                    cost=100,
                    max_products=1000000,
                    unlimited_products=True
                )

            subscription=Subscription.objects.create(
                business=branch.business,
                business_branch=branch,
                subscripton_package=package,
                amount=package.cost,
                subscription_type="Branch Subscription",
                active=False
            )

            SubscriptionPayment.objects.create(
                subscription=subscription,
                payer=branch.business.owner,
                amount_expected=subscription.amount
            )

            return Response(
                {"success": "Business branch created successfully!!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessBranchDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BusinessBranch.objects.all().order_by("-created_on")
    serializer_class = BusinessBranchSerializer

    permission_classes = [IsAuthenticated]

    lookup_field = "pk"

from django.urls import path
from payments.views import (
    SubscriptionPackageListCreateAPIView,
    SubscriptionListCreateAPIView,
    SubscriptionPackageDetailAPIView,
    SubscriptionDetailAPIView,
    SubscriptionPaymentAPIView,
    SubscriptionPaymentDetailAPIView,
    PaystackCallbackAPIView
)

urlpatterns = [
    path("", SubscriptionPaymentAPIView.as_view(), name="payments"),
    path("<int:pk>/", SubscriptionPaymentDetailAPIView.as_view(), name="payment-detail"),
    path("packages/", SubscriptionPackageListCreateAPIView.as_view(), name="packages"),
    path("packages/<int:pk>/", SubscriptionPackageDetailAPIView.as_view(), name="package-detail"),
    path("subscriptions/", SubscriptionListCreateAPIView.as_view(), name="subscriptions"),
    path("subscriptions/<int:pk>/", SubscriptionDetailAPIView.as_view(), name="subscription-detail"),
    path("paystack-callback/", PaystackCallbackAPIView.as_view(), name="paystack-callback"),
]

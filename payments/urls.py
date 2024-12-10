from django.urls import path
from payments.views import (
    SubscriptionPackageListCreateAPIView,
    SubscriptionAPIView,
    SubscriptionPackageDetailAPIView,
    SubscriptionDetailAPIView,
    SubscriptionPaymentAPIView,
    SubscriptionPaymentDetailAPIView,
    PaystackCallbackAPIView,
    SubscribeAPIView,
)

urlpatterns = [
    path("", SubscriptionPaymentAPIView.as_view(), name="payments"),
    path(
        "<int:pk>/", SubscriptionPaymentDetailAPIView.as_view(), name="payment-detail"
    ),
    path("packages/", SubscriptionPackageListCreateAPIView.as_view(), name="packages"),
    path(
        "packages/<int:pk>/",
        SubscriptionPackageDetailAPIView.as_view(),
        name="package-detail",
    ),
    path("subscriptions/", SubscriptionAPIView.as_view(), name="subscriptions"),
    path(
        "subscriptions/<int:pk>/",
        SubscriptionDetailAPIView.as_view(),
        name="subscription-detail",
    ),
    path(
        "paystack-callback/",
        PaystackCallbackAPIView.as_view(),
        name="paystack-callback",
    ),
    path("subscribe/", SubscribeAPIView.as_view(), name="subscribe"),
]

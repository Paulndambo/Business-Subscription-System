from rest_framework import serializers
from payments.models import SubscriptionPackage, Subscription, SubscriptionPayment


class SubscriptionPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPackage
        fields = "__all__"


class SubscriptionPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPayment
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class BusinessSubscriptionSerializer(serializers.Serializer):
    subscription_package = serializers.IntegerField()
    business = serializers.IntegerField()
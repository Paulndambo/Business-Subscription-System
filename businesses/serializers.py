from rest_framework import serializers
from businesses.models import Business, BusinessBranch


class BusinessBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessBranch
        fields = "__all__"


class BusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Business
        fields = "__all__"

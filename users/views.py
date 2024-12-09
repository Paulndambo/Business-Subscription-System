from django.shortcuts import render

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from users.serializers import RegisterUserSerializer, UsersSerializer
from users.models import User


# Create your views here.
class UsersListAPIView(generics.ListAPIView):
    queryset = User.objects.all().order_by("-created_on")
    serializer_class = UsersSerializer

    """
    Only a user who is an admin can see list of users on the application
    """
    permission_classes = [IsAdminUser]


class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            return Response(
                {"success": "User successfully registered!!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

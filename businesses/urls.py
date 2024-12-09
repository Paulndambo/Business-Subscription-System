from django.urls import path
from businesses.views import BusinessListAPIView

urlpatterns = [
    path("", BusinessListAPIView.as_view(), name="businesses"),
]

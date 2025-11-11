from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .models import Subscribers
from rest_framework.permissions import AllowAny
from .serializers import SubscribersSerializer

class SubscribersCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Subscribers.objects.all()
    serializer_class = SubscribersSerializer
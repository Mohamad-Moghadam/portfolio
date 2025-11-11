from django.shortcuts import render
from rest_framework.generics import CreateAPIView, DestroyAPIView
from .models import Subscribers
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import SubscribersSerializer

class SubscribersCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Subscribers.objects.all()
    serializer_class = SubscribersSerializer

class SignoutView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscribersSerializer

    def get_queryset(self):
        return Subscribers.objects.filter(id=self.request.user.id)
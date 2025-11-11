from django.urls import path
from .views import SubscribersCreateView, SignoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('subscribe', SubscribersCreateView.as_view(), name='subscribe'),
    path('signout', SignoutView.as_view(), name='signout'),
    path('token', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]

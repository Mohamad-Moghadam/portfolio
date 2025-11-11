from rest_framework.serializers import ModelSerializer
from .models import Subscribers


class SubscribersSerializer(ModelSerializer):
    class Meta:
        model = Subscribers
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
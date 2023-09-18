from rest_framework import serializers
from .models import subscriptionStatus



class subscriptionStatusserializer(serializers.ModelSerializer):
    class Meta:
        model = subscriptionStatus
        fields = "__all__"

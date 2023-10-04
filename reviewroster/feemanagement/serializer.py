from rest_framework import serializers
from .models import feestatus

class feestatusserializer(serializers.ModelSerializer):
    class Meta:
        model = feestatus
        fields = "__all__"

        
from rest_framework import serializers
from .models import Companies

class companySerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = "__all__"

        
from rest_framework import serializers
from .models import Calculation

class CalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calculation
        fields = '__all__'  # Adjust fields as needed

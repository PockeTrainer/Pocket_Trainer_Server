from rest_framework import serializers
from .models import DayHistoryDiet

class DayHistoryDietSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = DayHistoryDiet
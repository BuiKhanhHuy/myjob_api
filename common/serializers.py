from rest_framework import serializers
from .models import (
    Career,
    District
)


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'name', 'city')


class ProfileDistrictSerializers(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'name')

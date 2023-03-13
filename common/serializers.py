from rest_framework import serializers
from .models import (
    Career,
    Location,
    District
)


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'name', 'city')


class ProfileLocationSerializer(serializers.ModelSerializer):
    district = DistrictSerializer()

    class Meta:
        model = Location
        fields = ('id', 'address', 'district')

from rest_framework import serializers
from .models import (
    Career,
    District,
    Location
)


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'name', 'city')


class ProfileDistrictSerializers(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'name')


class ProfileLocationSerializer(serializers.ModelSerializer):
    districtDict = ProfileDistrictSerializers(source="district", read_only=True)

    class Meta:
        model = Location
        fields = ('city', 'districtDict', 'address', 'district')


class LocationSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=True, max_length=255)
    lat = serializers.FloatField(required=False, allow_null=True)
    lng = serializers.FloatField(required=False, allow_null=True)

    class Meta:
        model = Location
        fields = ('city', 'district', 'address', 'lat', 'lng')

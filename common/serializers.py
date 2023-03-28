from rest_framework import serializers
from .models import (
    District,
    Location,
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

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Location
        fields = ('city', 'district', 'address', 'lat', 'lng')

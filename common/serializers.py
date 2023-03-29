from rest_framework import serializers
from .models import (
    District,
    Location,
    Career
)


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'name', 'city')


class CareerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=150)
    iconUrl = serializers.URLField(source='icon_url', max_length=300)
    createAt = serializers.DateTimeField(source='create_at')
    updateAt = serializers.DateTimeField(source='update_at')
    jobPostTotal = serializers.SerializerMethodField(method_name='get_job_post_total')

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_job_post_total(self, career):
        return career.job_posts.count()

    class Meta:
        model = Career
        fields = ('id', 'name', 'iconUrl', 'createAt', 'updateAt', 'jobPostTotal')


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

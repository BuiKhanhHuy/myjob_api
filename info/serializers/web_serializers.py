from configs import variable_system as var_sys
from helpers import helper
from rest_framework import serializers
from ..models import JobSeekerProfile

from common import serializers as common_serializers
from authentication import serializers as auth_serializers


class ProfileSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()
    coverImageUrl = serializers.URLField(source="cover_image_url")
    isActive = serializers.BooleanField(source='is_active')

    def get_completed(self, profile):
        return 1

    class Meta:
        model = JobSeekerProfile
        fields = ("coverImageUrl", "isActive", "completed")


class ProfileDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    user = auth_serializers.ProfileUserSerializer()
    phone = serializers.CharField()
    birthday = serializers.DateField()
    gender = serializers.CharField()
    maritalStatus = serializers.CharField(source="marital_status")
    location = common_serializers.ProfileLocationSerializer()
    description = serializers.CharField()

    class Meta:
        model = JobSeekerProfile
        fields = ('title', 'user', 'phone', 'birthday',
                  'gender', 'maritalStatus',
                  'career', 'location', 'description')


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = "__all__"

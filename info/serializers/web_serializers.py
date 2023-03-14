from configs import variable_system as var_sys
from helpers import helper
from rest_framework import serializers
from ..models import (
    JobSeekerProfile, ExperienceDetail, EducationDetail
)

from authentication import serializers as auth_serializers
from common import serializers as common_serializers


class ProfileSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()
    coverImageUrl = serializers.URLField(source="cover_image_url")
    isActive = serializers.BooleanField(source='is_active')

    def get_completed(self, profile):
        return 1

    class Meta:
        model = JobSeekerProfile
        fields = ("coverImageUrl", "isActive", "completed")


class ProfileUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=200)
    fullName = serializers.CharField(required=True, max_length=100)
    email = serializers.CharField(required=True, max_length=100)
    phone = serializers.CharField(required=True, max_length=15)
    birthday = serializers.DateField(required=True, input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                                   var_sys.DATE_TIME_FORMAT["Ymd"]])
    gender = serializers.CharField(required=True, max_length=1)
    maritalStatus = serializers.CharField(source='marital_status',
                                          required=True,
                                          max_length=1)
    address = serializers.CharField(required=True, max_length=255)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = JobSeekerProfile
        fields = ('title', 'fullName', 'email',
                  'phone', 'birthday',
                  'gender', 'maritalStatus',
                  'city', 'district', 'address',
                  'career', 'description')


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = auth_serializers.ProfileUserSerializer()
    district = common_serializers.ProfileDistrictSerializers()
    maritalStatus = serializers.CharField(source="marital_status")

    class Meta:
        model = JobSeekerProfile
        fields = ('title', 'user', 'phone', 'birthday',
                  'gender', 'maritalStatus',
                  'city', 'district', 'address',
                  'career', 'description')


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = "__all__"


class ExperienceListSerializer(serializers.ModelSerializer):
    jobName = serializers.CharField(source='job_name')
    companyName = serializers.CharField(source='company_name')
    startDate = serializers.DateField(source='start_date')
    endDate = serializers.DateField(source='end_date')
    position = serializers.PrimaryKeyRelatedField(read_only=True)
    description = serializers.CharField()

    class Meta:
        model = ExperienceDetail
        fields = ('jobName', 'companyName', 'startDate', 'endDate',
                  'position', 'description')

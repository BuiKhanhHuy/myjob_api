from configs import variable_system as var_sys
from helpers import helper
from rest_framework import serializers
from ..models import (
    JobSeekerProfile,
    EducationDetail, ExperienceDetail,
    Certificate, LanguageSkill
)
from common.models import (
    Location
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
    phone = serializers.CharField(required=True, max_length=15)
    birthday = serializers.DateField(required=True, input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                                   var_sys.DATE_TIME_FORMAT["Ymd"]])
    gender = serializers.CharField(required=True, max_length=1)
    maritalStatus = serializers.CharField(source='marital_status',
                                          required=True,
                                          max_length=1)
    user = auth_serializers.ProfileUserSerializer()
    location = common_serializers.LocationSerializer()
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = JobSeekerProfile
        fields = ('title',
                  'phone', 'birthday',
                  'gender', 'maritalStatus',
                  'user', 'location',
                  'career', 'description')

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.marital_status = validated_data.get('marital_status', instance.marital_status)
        instance.career = validated_data.get('career', instance.career)
        instance.description = validated_data.get('description', instance.description)
        location_obj = instance.location
        user = instance.user
        if user:
            user.full_name = validated_data['user'].get('full_name', user.full_name)
            user.save()
        if location_obj:
            location_obj.city = validated_data["location"].get("city", location_obj.city)
            location_obj.district = validated_data["location"].get("district", location_obj.district)
            location_obj.address = validated_data["location"].get("address", location_obj.address)
            location_obj.save()
        else:
            location_new = Location.objects.create(**validated_data["location"])
            instance.location = location_new
        instance.save()
        return instance


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = auth_serializers.ProfileUserSerializer()
    maritalStatus = serializers.CharField(source="marital_status")
    location = common_serializers.ProfileLocationSerializer()

    class Meta:
        model = JobSeekerProfile
        fields = ('title', 'user', 'phone', 'birthday',
                  'gender', 'maritalStatus',
                  'location',
                  'career', 'description')


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = "__all__"


class EducationListCreateRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    degreeName = serializers.CharField(source='degree_name', required=True, max_length=200)
    major = serializers.CharField(required=True, max_length=255)
    trainingPlaceName = serializers.CharField(source='training_place_name', required=True, max_length=255)
    startDate = serializers.DateField(source='start_date', required=True)
    completedDate = serializers.DateField(source='completed_date', required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = EducationDetail
        fields = ('id', 'degreeName', 'major', 'trainingPlaceName',
                  'startDate', 'completedDate', 'description')

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        if user.is_authenticated:
            education_detail = EducationDetail.objects.create(**validated_data,
                                                              job_seeker_profile=user.job_seeker_profile)
            return education_detail
        return None


class ExperienceListCreateRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    jobName = serializers.CharField(source='job_name', required=True, max_length=200)
    companyName = serializers.CharField(source='company_name', required=True, max_length=255)
    startDate = serializers.DateField(source='start_date', required=True)
    endDate = serializers.DateField(source='end_date', required=True)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = ExperienceDetail
        fields = ('id', 'jobName', 'companyName', 'position',
                  'startDate', 'endDate',
                  'description')

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        if user.is_authenticated:
            experience_detail = ExperienceDetail.objects.create(**validated_data,
                                                                job_seeker_profile=user.job_seeker_profile)
            return experience_detail
        return None


class CertificateListCreateRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200)
    trainingPlace = serializers.CharField(source='training_place', required=True, max_length=255)
    startDate = serializers.DateField(source='start_date', required=True)
    expirationDate = serializers.DateField(source='expiration_date', required=False, allow_null=True)

    class Meta:
        model = Certificate
        fields = ('id', 'name', 'trainingPlace', 'startDate',
                  'expirationDate')

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        if user.is_authenticated:
            certificate_detail = Certificate.objects.create(**validated_data,
                                                            job_seeker_profile=user.job_seeker_profile)
            return certificate_detail
        return None


class LanguageSkillListCreateRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    language = serializers.IntegerField(required=True)
    level = serializers.IntegerField(required=True)

    class Meta:
        model = LanguageSkill
        fields = ('id', 'language', 'level')

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        if user.is_authenticated:
            language_skill = LanguageSkill.objects.create(**validated_data,
                                                          job_seeker_profile=user.job_seeker_profile)
            return language_skill
        return None

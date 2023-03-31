from configs import variable_system as var_sys
from helpers import helper
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.db import transaction
from .models import (
    JobPost,
    SavedJobPost,
    JobPostActivity
)
from common.models import (
    Location
)
from authentication import serializers as auth_serializers
from common import serializers as common_serializers
from info import serializers as info_serializers


class JobPostSerializer(serializers.ModelSerializer):
    jobName = serializers.CharField(source="job_name", required=True, max_length=255)
    deadline = serializers.DateField(required=True,
                                     input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                    var_sys.DATE_TIME_FORMAT["Ymd"]])
    quantity = serializers.IntegerField(required=True)
    genderRequired = serializers.CharField(source="gender_required", required=False,
                                           max_length=1, allow_blank=True, allow_null=True)
    jobDescription = serializers.CharField(source="job_description", required=True)
    jobRequirement = serializers.CharField(source="job_requirement", required=True)
    benefitsEnjoyed = serializers.CharField(source="benefits_enjoyed", required=True)

    position = serializers.IntegerField(required=True)
    typeOfWorkplace = serializers.IntegerField(source="type_of_workplace", required=True)
    experience = serializers.IntegerField(required=True)
    academicLevel = serializers.IntegerField(source='academic_level', required=True)
    jobType = serializers.IntegerField(source="job_type", required=True)
    salaryMin = serializers.IntegerField(source="salary_min", required=True)
    salaryMax = serializers.IntegerField(source="salary_max", required=True)
    isHot = serializers.BooleanField(source="is_hot", required=False, allow_null=True, read_only=True)
    isUrgent = serializers.BooleanField(source="is_urgent", default=False)
    contactPersonName = serializers.CharField(source="contact_person_name", required=True, max_length=100)
    contactPersonPhone = serializers.CharField(source="contact_person_phone", required=True, max_length=15)
    contactPersonEmail = serializers.EmailField(source="contact_person_email", required=True, max_length=100)
    createAt = serializers.DateTimeField(source="create_at", read_only=True)
    location = common_serializers.LocationSerializer()

    companyDict = info_serializers.CompanySerializer(source='company',
                                                     fields=['id', 'slug', 'employeeSize',
                                                             'companyImageUrl', 'companyName'],
                                                     read_only=True)
    locationDict = common_serializers.LocationSerializer(source="location",
                                                         fields=['city'],
                                                         read_only=True)

    views = serializers.IntegerField(read_only=True)
    appliedNumber = serializers.SerializerMethodField(method_name="get_applied_number", read_only=True)

    isSaved = serializers.SerializerMethodField(method_name='check_saved', read_only=True)
    isApplied = serializers.SerializerMethodField(method_name='check_applied', read_only=True)

    def get_applied_number(self, job_post):
        return job_post.peoples_applied.count()

    def check_saved(self, job_post):
        request = self.context.get('request', None)
        if request is None:
            return None
        user = request.user
        if user.is_authenticated:
            return job_post.savedjobpost_set.filter(user=user).exists()
        return None

    def check_applied(self, job_post):
        request = self.context.get('request', None)
        if request is None:
            return None
        user = request.user
        if user.is_authenticated:
            return job_post.jobpostactivity_set.filter(user=user).count() > 0
        return None

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = JobPost
        fields = ('id', 'slug', 'jobName', 'deadline', 'quantity', 'genderRequired',
                  'jobDescription', 'jobRequirement', 'benefitsEnjoyed', 'career',
                  'position', 'typeOfWorkplace', 'experience', 'academicLevel',
                  'jobType', 'salaryMin', 'salaryMax', 'isHot', 'isUrgent',
                  'contactPersonName', 'contactPersonPhone', 'contactPersonEmail',
                  'location', 'createAt', 'appliedNumber',
                  'isSaved', 'isApplied', 'companyDict', 'locationDict', 'views')

    def create(self, validated_data):
        try:
            request = self.context['request']
            user = request.user
            company = user.company

            location_data = validated_data.pop('location')
            location = Location(**location_data)

            job_post = JobPost(**validated_data)
            with transaction.atomic():
                location.save()
                job_post.location = location
                job_post.user = user
                job_post.company = company
                job_post.save()
        except Exception as ex:
            helper.print_log_error("create job post", error=ex)
            return None
        else:
            return job_post

    def update(self, instance, validated_data):
        try:
            instance.job_name = validated_data.get('job_name', instance.job_name)
            instance.deadline = validated_data.get('deadline', instance.deadline)
            instance.quantity = validated_data.get('quantity', instance.quantity)
            instance.gender_required = validated_data.get('gender_required', instance.gender_required)
            instance.job_description = validated_data.get('job_description', instance.job_description)
            instance.job_requirement = validated_data.get('job_requirement', instance.job_requirement)
            instance.benefits_enjoyed = validated_data.get('benefits_enjoyed', instance.benefits_enjoyed)
            instance.position = validated_data.get('position', instance.position)
            instance.type_of_workplace = validated_data.get('type_of_workplace', instance.type_of_workplace)
            instance.experience = validated_data.get('experience', instance.experience)
            instance.academic_level = validated_data.get('academic_level', instance.academic_level)
            instance.job_type = validated_data.get('job_type', instance.job_type)
            instance.salary_min = validated_data.get('salary_min', instance.salary_min)
            instance.salary_max = validated_data.get('salary_max', instance.salary_max)
            instance.is_urgent = validated_data.get('is_urgent', instance.is_urgent)
            instance.contact_person_name = validated_data.get('contact_person_name', instance.contact_person_name)
            instance.contact_person_phone = validated_data.get('contact_person_phone', instance.contact_person_phone)
            instance.contact_person_email = validated_data.get('contact_person_email', instance.contact_person_email)
            location_obj = instance.location

            with transaction.atomic():
                if location_obj:
                    location_obj.city = validated_data["location"].get("city", location_obj.city)
                    location_obj.district = validated_data["location"].get("district", location_obj.district)
                    location_obj.address = validated_data["location"].get("address", location_obj.address)
                    location_obj.lat = validated_data["location"].get("lat", location_obj.lat)
                    location_obj.lng = validated_data["location"].get("lng", location_obj.lng)
                    location_obj.save()
                instance.save()
                return instance
        except Exception as ex:
            helper.print_log_error("update job post", ex)
            return None

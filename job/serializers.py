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


class JobPostSerializer(serializers.ModelSerializer):
    jobName = serializers.CharField(source="job_name", required=True, max_length=255)
    deadline = serializers.DateField(required=True)
    quantity = serializers.IntegerField(required=True)
    genderRequired = serializers.CharField(source="gender_required", required=False,
                                           max_length=1, allow_blank=True, allow_null=True)
    jobDescription = serializers.CharField(source="job_description", required=True)
    jobRequirement = serializers.CharField(source="job_requirement", required=True)
    benefitsEnjoyed = serializers.CharField(source="benefits_enjoyed", required=True)

    position = serializers.IntegerField(required=True)
    typeOfWorkplace = serializers.IntegerField(source="type_of_workplace", required=True)
    experience = serializers.IntegerField(required=True)
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

    viewNumber = serializers.SerializerMethodField(method_name="get_view_number", read_only=True)

    def get_view_number(self, job_post):
        return 1000

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
        fields = ('id', 'jobName', 'deadline', 'quantity', 'genderRequired',
                  'jobDescription', 'jobRequirement', 'benefitsEnjoyed',
                  'position', 'typeOfWorkplace', 'experience',
                  'jobType', 'salaryMin', 'salaryMax', 'isHot', 'isUrgent',
                  'contactPersonName', 'contactPersonPhone', 'contactPersonEmail',
                  'location', 'createAt', 'viewNumber')

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

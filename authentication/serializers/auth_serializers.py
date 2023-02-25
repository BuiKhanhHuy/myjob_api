from configs import variable_system as var_sys
from helpers import helper
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.db import transaction
from ..models import User
from common.models import Location, District
from info.models import JobSeekerProfile, Company


class JobSeekerRegisterSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source="full_name", required=True, max_length=100)
    email = serializers.EmailField(required=True, max_length=100,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True, max_length=100)

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = User.objects.create_user_with_role_name(**validated_data,
                                                               is_active=False,
                                                               role_name=var_sys.JOB_SEEKER)
                JobSeekerProfile.objects.create(user=user)

                return user
        except Exception as ex:
            helper.print_log_error("create user in JobSeekerRegisterSerializer", ex)
            return None

    class Meta:
        model = User
        fields = ("fullName", "email", "password")


class CompanyRegisterSerializer(serializers.ModelSerializer):
    companyName = serializers.CharField(source="company_name", required=True, max_length=255,
                                        validators=[UniqueValidator(Company.objects.all())])
    email = serializers.EmailField(required=True, max_length=100,
                                   validators=[UniqueValidator(Company.objects.all())])
    phone = serializers.CharField(required=False, max_length=15,
                                  validators=[UniqueValidator(Company.objects.all())])
    taxCode = serializers.CharField(source="tax_code", required=True, max_length=30,
                                    validators=[UniqueValidator(Company.objects.all())])
    fieldOperation = serializers.CharField(source="field_operation", required=False,
                                           max_length=255)
    districtId = serializers.IntegerField(required=True)
    since = serializers.DateField(required=False)
    address = serializers.CharField(required=True, max_length=255)
    employeeSize = serializers.IntegerField(source="employee_size", required=True)
    websiteUrl = serializers.URLField(source="website_url", required=False,
                                      max_length=300)
    description = serializers.CharField(required=False)

    class Meta:
        model = Company
        fields = ("companyName", "email", "phone",
                  "taxCode", "fieldOperation", "since",
                  "districtId",
                  "address",
                  "employeeSize",
                  "websiteUrl", "description")


class EmployerRegisterSerializer(serializers.ModelSerializer):
    company = CompanyRegisterSerializer()
    fullName = serializers.CharField(source="full_name", required=True, max_length=100)
    email = serializers.EmailField(required=True, max_length=100,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True, max_length=100)

    def create(self, validated_data):
        try:
            with transaction.atomic():
                company = validated_data.pop("company")
                district_id = company.pop("districtId")
                address = company.pop("address")

                user = User.objects.create_user_with_role_name(**validated_data,
                                                               is_active=False,
                                                               has_company=True,
                                                               role_name=var_sys.EMPLOYER)
                location = Location.objects.create(address=address,
                                                   district=District.objects.get(pk=district_id))
                Company.objects.create(user=user, location=location, **company)

                return validated_data
        except Exception as ex:
            helper.print_log_error("create user in JobSeekerRegisterSerializer", ex)
            return None

    class Meta:
        model = User
        fields = ("fullName", "email", "password", "company")


class UserInfoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    isActive = serializers.BooleanField(source="is_active")
    fullName = serializers.CharField(source="full_name")
    email = serializers.CharField()
    avatarUrl = serializers.URLField(source="avatar_url")
    phone = serializers.CharField()
    birthday = serializers.DateField()
    gender = serializers.CharField()
    emailNotificationActive = serializers.BooleanField(source="email_notification_active")
    smsNotificationActive = serializers.BooleanField(source="sms_notification_active")
    roleName = serializers.CharField(source="role_name")

    class Meta:
        model = User
        fields = ("id", "isActive", "fullName", "email", "avatarUrl",
                  "phone", "birthday", "gender", "emailNotificationActive",
                  "smsNotificationActive", "roleName", "job_seeker_profile",
                  "company")

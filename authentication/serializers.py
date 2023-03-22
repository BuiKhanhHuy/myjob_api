import datetime

from configs import variable_system as var_sys
from helpers import helper
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.db import transaction
from .models import User
from info.models import (
    JobSeekerProfile, Resume,
    Company
)
from common.models import Location
from common.serializers import LocationSerializer


class CheckCredsSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=100)
    roleName = serializers.CharField(required=False, max_length=10,
                                     allow_null=True, allow_blank=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=100)
    roleName = serializers.CharField(required=True, max_length=10)


class ResetPasswordSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(required=True, max_length=128)
    newPassword = serializers.CharField(required=True, max_length=128)
    confirmPassword = serializers.CharField(required=True, max_length=128)

    def validate(self, attrs):
        user = self.context['user']

        old_pass = attrs.get('oldPassword', '')
        new_pass = attrs.get('newPassword', '')
        confirm_pass = attrs.get('confirmPassword', '')
        if not new_pass == confirm_pass:
            raise serializers.ValidationError({'confirmPassword': 'Mật khẩu xác nhận không chính xác.'})

        if not user.check_password(old_pass):
            raise serializers.ValidationError({'oldPassword': 'Mật khẩu hiện tại không chính xác.'})
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('newPassword'))
        instance.save()

        return instance


class JobSeekerRegisterSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source="full_name", required=True, max_length=100)
    email = serializers.EmailField(required=True, max_length=100,
                                   validators=[UniqueValidator(queryset=User.objects.all(),
                                                               message="Email đã tồn tại.")])
    password = serializers.CharField(required=True, max_length=100)
    confirmPassword = serializers.CharField(required=True, max_length=100)

    def validate(self, attrs):
        if not attrs["password"] == attrs["confirmPassword"]:
            raise serializers.ValidationError({'confirmPassword': 'Mật khẩu xác nhận không chính xác.'})
        return attrs

    def create(self, validated_data):
        try:
            with transaction.atomic():
                validated_data.pop("confirmPassword")
                user = User.objects.create_user_with_role_name(**validated_data,
                                                               is_active=False,
                                                               role_name=var_sys.JOB_SEEKER)
                job_seeker_profile = JobSeekerProfile.objects.create(user=user)
                Resume.objects.create(job_seeker_profile=job_seeker_profile, user=user,
                                      type=var_sys.CV_WEBSITE)

                return user
        except Exception as ex:
            helper.print_log_error("create user in JobSeekerRegisterSerializer", ex)
            return None

    class Meta:
        model = User
        fields = ("fullName", "email", "password", "confirmPassword")


class CompanyRegisterSerializer(serializers.ModelSerializer):
    companyName = serializers.CharField(source="company_name", required=True, max_length=255,
                                        validators=[UniqueValidator(Company.objects.all(),
                                                                    message='Tên công ty đã tồn tại.')])
    companyEmail = serializers.EmailField(source='company_email', required=True, max_length=100,
                                          validators=[UniqueValidator(Company.objects.all(),
                                                                      message='Email công ty đã tồn tại.')])
    companyPhone = serializers.CharField(source='company_phone', required=False, max_length=15,
                                         validators=[UniqueValidator(Company.objects.all(),
                                                                     message='Số điện thoại công ty đã tồn tại.')])
    taxCode = serializers.CharField(source="tax_code", required=True, max_length=30,
                                    validators=[UniqueValidator(Company.objects.all(),
                                                                message='Mã số thuế công ty đã tồn tại.')])
    fieldOperation = serializers.CharField(source="field_operation", required=False,
                                           max_length=255,
                                           allow_null=True,
                                           allow_blank=True)
    since = serializers.DateField(required=False,
                                  input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                 var_sys.DATE_TIME_FORMAT["Ymd"]],
                                  allow_null=True)
    employeeSize = serializers.IntegerField(source="employee_size", required=True)
    websiteUrl = serializers.URLField(source="website_url", required=False, max_length=300,
                                      allow_blank=True,
                                      allow_null=True)
    description = serializers.CharField(required=False)
    location = LocationSerializer()

    class Meta:
        model = Company
        fields = ("companyName", "companyEmail", "companyPhone",
                  "taxCode", "fieldOperation", "since",
                  "employeeSize",
                  "websiteUrl", "description",
                  "location")


class EmployerRegisterSerializer(serializers.ModelSerializer):
    company = CompanyRegisterSerializer()
    fullName = serializers.CharField(source="full_name", required=True, max_length=100)
    email = serializers.EmailField(required=True, max_length=100,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True, max_length=100)
    confirmPassword = serializers.CharField(required=True, max_length=100)

    def validate(self, attrs):
        if not attrs["password"] == attrs["confirmPassword"]:
            raise serializers.ValidationError({'confirmPassword': 'Mật khẩu xác nhận không chính xác!'})
        return attrs

    def create(self, validated_data):
        try:
            with transaction.atomic():
                validated_data.pop("confirmPassword")
                company = validated_data.pop("company")
                location = company.pop("location")

                location_obj = Location.objects.create(**location)
                user = User.objects.create_user_with_role_name(**validated_data,
                                                               is_active=False,
                                                               has_company=True,
                                                               role_name=var_sys.EMPLOYER)
                Company.objects.create(user=user, **company, location=location_obj)

                return validated_data
        except Exception as ex:
            helper.print_log_error("create user in JobSeekerRegisterSerializer", ex)
            return None

    class Meta:
        model = User
        fields = ("fullName", "email", "password", "confirmPassword", "company")


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    fullName = serializers.CharField(source="full_name")
    email = serializers.CharField()
    avatarUrl = serializers.URLField(source="avatar_url")
    isActive = serializers.BooleanField(source='is_active')
    isVerifyEmail = serializers.BooleanField(source='is_verify_email')
    roleName = serializers.CharField(source="role_name")
    jobSeekerProfileId = serializers.PrimaryKeyRelatedField(source='job_seeker_profile',
                                                            read_only=True)
    companyId = serializers.PrimaryKeyRelatedField(source='company', read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = User
        fields = ("id", "fullName", "email",
                  "isActive", "isVerifyEmail",
                  "avatarUrl", "roleName",
                  "jobSeekerProfileId",
                  "companyId")

import cloudinary.uploader

from configs import variable_system as var_sys
from helpers import helper
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.conf import settings
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
    platform = serializers.CharField(required=True)

    def validate_platform(self, platform):
        if platform not in ["WEB", "APP"]:
            raise serializers.ValidationError("platform không hợp lệ.")
        return platform


class UpdatePasswordSerializer(serializers.Serializer):
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


class ResetPasswordSerializer(serializers.Serializer):
    newPassword = serializers.CharField(required=True, max_length=128)
    confirmPassword = serializers.CharField(required=True, max_length=128)
    token = serializers.CharField(required=False)
    code = serializers.CharField(required=False)
    platform = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def validate(self, attrs):
        new_pass = attrs.get('newPassword', '')
        confirm_pass = attrs.get('confirmPassword', '')
        if not new_pass == confirm_pass:
            raise serializers.ValidationError({'confirmPassword': 'Mật khẩu xác nhận không chính xác.'})

        platform = attrs.get("platform", "")
        if platform not in ["APP", "WEB"]:
            raise serializers.ValidationError({'platform': 'platform không hợp lệ.'})
        if platform == "APP":
            if not attrs.get("code", None):
                raise serializers.ValidationError({'code': 'code là bắt buộc.'})
        elif platform == "WEB":
            if not attrs.get("token", None):
                raise serializers.ValidationError({'token': 'token là bắt buộc.'})
        return attrs


class JobSeekerRegisterSerializer(serializers.Serializer):
    fullName = serializers.CharField(source="full_name", required=True, max_length=100)
    email = serializers.EmailField(required=True, max_length=100,
                                   validators=[UniqueValidator(queryset=User.objects.all(),
                                                               message="Email đã tồn tại.")])
    password = serializers.CharField(required=True, max_length=100)
    confirmPassword = serializers.CharField(required=True, max_length=100)
    platform = serializers.CharField(required=True, max_length=3)

    def validate(self, attrs):
        if not attrs["password"] == attrs["confirmPassword"]:
            raise serializers.ValidationError({'confirmPassword': 'Mật khẩu xác nhận không chính xác.'})
        return attrs

    def create(self, validated_data):
        try:
            with transaction.atomic():
                validated_data.pop("confirmPassword")
                validated_data.pop("platform")
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
        fields = ("fullName", "email", "password", "confirmPassword", "platform")


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


class EmployerRegisterSerializer(serializers.Serializer):
    company = CompanyRegisterSerializer()
    fullName = serializers.CharField(source="full_name", required=True, max_length=100)
    email = serializers.EmailField(required=True, max_length=100,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True, max_length=100)
    confirmPassword = serializers.CharField(required=True, max_length=100)
    platform = serializers.CharField(required=True, max_length=3)

    def validate(self, attrs):
        if not attrs["password"] == attrs["confirmPassword"]:
            raise serializers.ValidationError({'confirmPassword': 'Mật khẩu xác nhận không chính xác!'})
        return attrs

    def create(self, validated_data):
        try:
            with transaction.atomic():
                validated_data.pop("confirmPassword")
                validated_data.pop("platform")
                company = validated_data.pop("company")
                location = company.pop("location")

                location_obj = Location.objects.create(**location)
                user = User.objects.create_user_with_role_name(**validated_data,
                                                               is_active=False,
                                                               has_company=True,
                                                               role_name=var_sys.EMPLOYER)
                Company.objects.create(user=user, **company, location=location_obj)

                return user
        except Exception as ex:
            helper.print_log_error("create user in JobSeekerRegisterSerializer", ex)
            return None

    class Meta:
        model = User
        fields = ("fullName", "email", "password", "confirmPassword", "company", "platform")


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
    jobSeekerProfile = serializers.SerializerMethodField(method_name="get_job_seeker_profile", read_only=True)
    companyId = serializers.PrimaryKeyRelatedField(source='company', read_only=True)
    company = serializers.SerializerMethodField(method_name='get_company')

    def get_job_seeker_profile(self, user):
        if user.role_name == var_sys.JOB_SEEKER:
            job_seeker_profile = user.job_seeker_profile
            return {
                "id": job_seeker_profile.id,
                "phone": job_seeker_profile.phone
            }
        return None

    def get_company(self, user):
        if user.role_name == var_sys.EMPLOYER:
            company = user.company
            return {
                "id": company.id,
                "slug": company.slug,
                "companyName": company.company_name,
                "imageUrl": company.company_image_url
            }
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
        model = User
        fields = ("id", "fullName", "email",
                  "isActive", "isVerifyEmail",
                  "avatarUrl", "roleName",
                  "jobSeekerProfileId", "jobSeekerProfile",
                  "companyId", "company",)


class AvatarSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True, write_only=True)
    avatarUrl = serializers.CharField(source="avatar_url",
                                      required=False,
                                      max_length=300,
                                      read_only=True)

    def update(self, user, validated_data):
        file = validated_data.pop('file')

        try:
            avatar_upload_result = cloudinary.uploader.upload(file,
                                                              folder=settings.CLOUDINARY_DIRECTORY["avatar"],
                                                              public_id=user.id)
            avatar_public_id = avatar_upload_result.get('public_id')
        except:
            return None
        else:
            avatar_url = avatar_upload_result.get('secure_url')
            user.avatar_url = avatar_url
            user.avatar_public_id = avatar_public_id
            user.save()

            return user

    class Meta:
        model = User
        fields = ('file', 'avatarUrl')

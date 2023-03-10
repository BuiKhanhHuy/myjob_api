from configs import variable_system as var_sys
from helpers import helper
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.db import transaction
from .models import User
from common.models import Location, District
from info.models import JobSeekerProfile, Company


class CheckCredsSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=100)
    roleName = serializers.CharField(required=True, max_length=10)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=100)
    roleName = serializers.CharField(required=True, max_length=10)


class ResetPasswordSerializer(serializers.Serializer):
    newPassword = serializers.CharField(required=True, max_length=128)


class JobSeekerRegisterSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source="full_name", required=True, max_length=100)
    email = serializers.EmailField(required=True, max_length=100,
                                   validators=[UniqueValidator(queryset=User.objects.all(),
                                                               message="Email đã tồn tại!")])
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
        fields = ("fullName", "email", "password", "confirmPassword")


class CompanyRegisterSerializer(serializers.ModelSerializer):
    companyName = serializers.CharField(source="company_name", required=True, max_length=255,
                                        validators=[UniqueValidator(Company.objects.all(),
                                                                    message='Tên công ty đã tồn tại!')])
    companyEmail = serializers.EmailField(required=True, max_length=100,
                                          validators=[UniqueValidator(Company.objects.all(),
                                                                      message='Email công ty đã tồn tại.')])
    companyPhone = serializers.CharField(required=False, max_length=15,
                                         validators=[UniqueValidator(Company.objects.all(),
                                                                     message='Số điện thoại công ty đã tồn tại.')])
    taxCode = serializers.CharField(source="tax_code", required=True, max_length=30,
                                    validators=[UniqueValidator(Company.objects.all(),
                                                                message='Mã số thuế công ty đã tồn tại.')])
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
        fields = ("companyName", "companyEmail", "companyPhone",
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
        fields = ("fullName", "email", "password", "confirmPassword", "company")


class UserInfoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    fullName = serializers.CharField(source="full_name")
    email = serializers.CharField()
    avatarUrl = serializers.URLField(source="avatar_url")
    roleName = serializers.CharField(source="role_name")

    class Meta:
        model = User
        fields = ("id", "fullName", "email",
                  "avatarUrl", "roleName")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

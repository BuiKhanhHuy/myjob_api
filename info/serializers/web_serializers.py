from configs import variable_system as var_sys
from helpers import helper
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.db import transaction
from ..models import (
    JobSeekerProfile,
    EducationDetail, ExperienceDetail,
    Certificate, LanguageSkill,
    AdvancedSkill,
    Company
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
    user = auth_serializers.UserRetrieveUpdateSerializer()
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
    user = auth_serializers.UserRetrieveUpdateSerializer()
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
    startDate = serializers.DateField(source='start_date', required=True,
                                      input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                     var_sys.DATE_TIME_FORMAT["Ymd"]])
    completedDate = serializers.DateField(source='completed_date', required=False, allow_null=True,
                                          input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                         var_sys.DATE_TIME_FORMAT["Ymd"]])
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = EducationDetail
        fields = ('id', 'degreeName', 'major', 'trainingPlaceName',
                  'startDate', 'completedDate', 'description')

    def validate(self, attrs):
        if EducationDetail.objects.count() >= 10:
            raise serializers.ValidationError({'errorMessage': 'Tối đa 10 thông tin học vấn'})
        return attrs

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
    startDate = serializers.DateField(source='start_date', required=True,
                                      input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                     var_sys.DATE_TIME_FORMAT["Ymd"]])
    endDate = serializers.DateField(source='end_date', required=True,
                                    input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                   var_sys.DATE_TIME_FORMAT["Ymd"]])
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def validate(self, attrs):
        if ExperienceDetail.objects.count() >= 10:
            raise serializers.ValidationError({'errorMessage': 'Tối đa 10 thông tin kinh nghiệm làm việc'})
        return attrs

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
    startDate = serializers.DateField(source='start_date', required=True,
                                      input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                     var_sys.DATE_TIME_FORMAT["Ymd"]])
    expirationDate = serializers.DateField(source='expiration_date', required=False, allow_null=True,
                                           input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                          var_sys.DATE_TIME_FORMAT["Ymd"]])

    def validate(self, attrs):
        if Certificate.objects.count() >= 10:
            raise serializers.ValidationError({'errorMessage': 'Tối đa 10 thông tin chứng chỉ'})
        return attrs

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

    def validate_language(self, language):
        request = self.context['request']

        if LanguageSkill.objects.filter(language=language,
                                        job_seeker_profile=request.user.job_seeker_profile).exists():
            raise serializers.ValidationError('Ngôn ngữ này đã tồn tại.')
        return language

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


class AdvancedSkillListCreateRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200)
    level = serializers.IntegerField(required=True)

    def validate_name(self, name):
        request = self.context['request']

        if AdvancedSkill.objects.filter(name__iexact=name,
                                        job_seeker_profile=request.user.job_seeker_profile).exists():
            raise serializers.ValidationError('Kỹ năng này đã tồn tại.')
        return name

    def validate(self, attrs):
        if AdvancedSkill.objects.count() >= 15:
            raise serializers.ValidationError({'errorMessage': 'Tối đa 15 thông tin kỹ năng chuyên môn'})
        return attrs

    class Meta:
        model = AdvancedSkill
        fields = ('id', 'name', 'level')

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        if user.is_authenticated:
            advanced_skill = AdvancedSkill.objects.create(**validated_data,
                                                          job_seeker_profile=user.job_seeker_profile)
            return advanced_skill
        return None


class CompanyRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    taxCode = serializers.CharField(source="tax_code", required=True, max_length=30,
                                    validators=[UniqueValidator(Company.objects.all(),
                                                                message="Mã số thuế công ty đã tồn tại.")])
    companyName = serializers.CharField(source="company_name", required=True,
                                        validators=[UniqueValidator(Company.objects.all(),
                                                                    message='Tên công ty đã tồn tại.')])
    employeeSize = serializers.IntegerField(source="employee_size", required=True)
    fieldOperation = serializers.CharField(source="field_operation", required=True,
                                           max_length=255)
    location = common_serializers.LocationSerializer()
    since = serializers.DateField(required=True, allow_null=True, input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                                   var_sys.DATE_TIME_FORMAT["Ymd"]])
    companyEmail = serializers.CharField(source="company_email", required=True,
                                         max_length=100, validators=[UniqueValidator(Company.objects.all(),
                                                                                     message='Email công ty đã tồn tại.')])
    companyPhone = serializers.CharField(source="company_phone", required=True,
                                         max_length=15, validators=[UniqueValidator(Company.objects.all(),
                                                                                    message='Số điện thoại công ty đã tồn tại.')])
    websiteUrl = serializers.URLField(required=False, source="website_url", max_length=300,
                                       allow_null=True, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Company
        fields = ('id', 'taxCode', 'companyName',
                  'employeeSize', 'fieldOperation', 'location',
                  'since', 'companyEmail', 'companyPhone',
                  'websiteUrl', 'description')

    def update(self, instance, validated_data):
        try:
            instance.tax_code = validated_data.get('tax_code', instance.tax_code)
            instance.company_name = validated_data.get('company_name', instance.company_name)
            instance.employee_size = validated_data.get('employee_size', instance.employee_size)
            instance.field_operation = validated_data.get('field_operation', instance.field_operation)
            instance.since = validated_data.get('since', instance.since)
            instance.company_email = validated_data.get('company_email', instance.company_email)
            instance.company_phone = validated_data.get('company_phone', instance.company_phone)
            instance.website_url = validated_data.get('website_url', instance.website_url)
            instance.description = validated_data.get('company_phone', instance.description)
            location_obj = instance.location

            with transaction.atomic():
                if location_obj:
                    location_obj.city = validated_data["location"].get("city", location_obj.city)
                    location_obj.district = validated_data["location"].get("district", location_obj.district)
                    location_obj.address = validated_data["location"].get("address", location_obj.address)
                    location_obj.lat = validated_data["location"].get("lat", location_obj.lat)
                    location_obj.lng = validated_data["location"].get("lng", location_obj.lng)
                    location_obj.save()
                else:
                    location_new = Location.objects.create(**validated_data["location"])
                    instance.location = location_new
                instance.save()
                return instance
        except Exception as ex:
            helper.print_log_error("update company", ex)
            return None

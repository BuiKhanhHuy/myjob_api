from datetime import date
import cloudinary.uploader
from django.conf import settings
from jsonschema._validators import required

from configs import variable_system as var_sys
from helpers import helper
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.db import transaction
from .models import (
    JobSeekerProfile,
    Resume, ResumeViewed,
    ResumeSaved,
    EducationDetail,
    ExperienceDetail,
    Certificate,
    LanguageSkill,
    AdvancedSkill,
    Company,
    CompanyFollowed,
    CompanyImage
)
from common.models import (
    Location
)

from authentication import serializers as auth_serializers
from common import serializers as common_serializers


class CompanyImageSerializer(serializers.ModelSerializer):
    imageUrl = serializers.CharField(source='image_url', required=False, read_only=True)
    files = serializers.ListField(required=True, write_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def validate(self, attrs):
        files = attrs.get("files", [])
        count_upload_file = len(files)

        request = self.context['request']
        user = request.user
        if user.role_name == var_sys.EMPLOYER:
            company = user.company
            if CompanyImage.objects.filter(company=company).count() + count_upload_file > 12:
                raise serializers.ValidationError({'errorMessage': 'Tối đa 12 ảnh'})
        return attrs

    def create(self, validated_data):
        files = validated_data.pop('files', [])
        request = self.context["request"]

        for file in files:
            company_image = CompanyImage.objects.create(company=request.user.company)
            company_image_upload_result = cloudinary.uploader.upload(
                file,
                folder=settings.CLOUDINARY_DIRECTORY[
                    "company_image"],
                public_id=company_image.id
            )
            company_image_public_id = company_image_upload_result.get('public_id')
            company_image_url = company_image_upload_result["secure_url"]

            company_image.image_url = company_image_url
            company_image.image_public_id = company_image_public_id
            company_image.save()

        return validated_data

    class Meta:
        model = CompanyImage
        fields = ('id', 'imageUrl', 'files')


class CompanySerializer(serializers.ModelSerializer):
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
                                         max_length=15, validators=[
            UniqueValidator(Company.objects.all(),
                            message='Số điện thoại công ty đã tồn tại.')
        ])
    websiteUrl = serializers.URLField(required=False, source="website_url", max_length=300,
                                      allow_null=True, allow_blank=True)
    facebookUrl = serializers.URLField(required=False, source="facebook_url", max_length=300,
                                       allow_null=True, allow_blank=True)
    youtubeUrl = serializers.URLField(required=False, source="youtube_url", max_length=300,
                                      allow_null=True, allow_blank=True)
    linkedinUrl = serializers.URLField(required=False, source="linkedin_url", max_length=300,
                                       allow_null=True, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    companyImageUrl = serializers.CharField(source='company_image_url', read_only=True)
    companyCoverImageUrl = serializers.URLField(source='company_cover_image_url', read_only=True)
    locationDict = common_serializers.LocationSerializer(source="location",
                                                         fields=['city'],
                                                         read_only=True)

    followNumber = serializers.SerializerMethodField(method_name="get_follow_number", read_only=True)
    jobPostNumber = serializers.SerializerMethodField(method_name="get_job_post_number", read_only=True)
    isFollowed = serializers.SerializerMethodField(method_name='check_followed', read_only=True)
    companyImages = CompanyImageSerializer(source='company_images', many=True, read_only=True,
                                           fields=['id', 'imageUrl'])

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_follow_number(self, company):
        return company.companyfollowed_set.filter().count()

    def get_job_post_number(self, company):
        return company.job_posts.count()

    def check_followed(self, company):
        request = self.context.get('request', None)
        if request is None:
            return None
        user = request.user
        if user.is_authenticated:
            return company.companyfollowed_set.filter(user=user).count() > 0
        return None

    class Meta:
        model = Company
        fields = ('id', 'slug', 'taxCode', 'companyName',
                  'employeeSize', 'fieldOperation', 'location',
                  'since', 'companyEmail', 'companyPhone',
                  'websiteUrl', 'facebookUrl', 'youtubeUrl', 'linkedinUrl',
                  'description',
                  'companyImageUrl', 'companyCoverImageUrl', 'locationDict',
                  'followNumber', 'jobPostNumber', 'isFollowed',
                  'companyImages')

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
            instance.facebook_url = validated_data.get('facebook_url', instance.facebook_url)
            instance.youtube_url = validated_data.get('youtube_url', instance.youtube_url)
            instance.linkedin_url = validated_data.get('linkedin_url', instance.linkedin_url)
            instance.description = validated_data.get('description', instance.description)
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


class CompanyFollowedSerializer(serializers.ModelSerializer):
    company = CompanySerializer(fields=['id', 'slug', 'companyName', 'companyImageUrl',
                                        'fieldOperation', 'followNumber', 'jobPostNumber'])

    class Meta:
        model = CompanyFollowed
        fields = (
            'id',
            'company',
        )


class LogoCompanySerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True, write_only=True)
    companyImageUrl = serializers.CharField(source='company_image_url', read_only=True)

    class Meta:
        model = Company
        fields = ('file', 'companyImageUrl')

    def update(self, company, validated_data):
        file = validated_data.pop('file')

        try:
            logo_upload_result = cloudinary.uploader.upload(file,
                                                            folder=settings.CLOUDINARY_DIRECTORY["logo"],
                                                            public_id=company.id)
            logo_public_id = logo_upload_result.get('public_id')
        except:
            return None
        else:
            logo_url = logo_upload_result.get('secure_url')
            company.company_image_url = logo_url
            company.company_image_public_id = logo_public_id
            company.save()

            return company


class CompanyCoverImageSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True, write_only=True)
    companyCoverImageUrl = serializers.CharField(source='company_cover_image_url', read_only=True)

    class Meta:
        model = Company
        fields = ('file', 'companyCoverImageUrl')

    def update(self, company, validated_data):
        file = validated_data.pop('file')

        try:
            company_cover_image_upload_result = cloudinary.uploader.upload(file,
                                                                           folder=settings.CLOUDINARY_DIRECTORY[
                                                                               "coverImage"],
                                                                           public_id=company.id)
            company_cover_image_public_id = company_cover_image_upload_result.get('public_id')
        except:
            return None
        else:
            company_cover_image_url = company_cover_image_upload_result.get('secure_url')
            company.company_cover_image_url = company_cover_image_url
            company.company_cover_image_public_id = company_cover_image_public_id
            company.save()

            return company


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True, max_length=15)
    birthday = serializers.DateField(required=True, input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                                   var_sys.DATE_TIME_FORMAT["Ymd"]])
    gender = serializers.CharField(required=True, max_length=1)
    maritalStatus = serializers.CharField(source='marital_status',
                                          required=True,
                                          max_length=1)
    location = common_serializers.ProfileLocationSerializer()
    user = auth_serializers.UserSerializer(fields=["fullName"])
    old = serializers.SerializerMethodField(method_name="get_old", read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_old(self, job_seeker_profile):
        birthdate = job_seeker_profile.birthday
        if birthdate:
            today = date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            return age
        return None

    class Meta:
        model = JobSeekerProfile
        fields = ('id', 'phone', 'birthday',
                  'gender', 'maritalStatus',
                  'location', 'user', 'old')

    def update(self, instance, validated_data):
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.marital_status = validated_data.get('marital_status', instance.marital_status)
        location_obj = instance.location
        user_obj = instance.user

        if location_obj:
            location_obj.city = validated_data["location"].get("city", location_obj.city)
            location_obj.district = validated_data["location"].get("district", location_obj.district)
            location_obj.address = validated_data["location"].get("address", location_obj.address)
            location_obj.save()
        else:
            location_new = Location.objects.create(**validated_data["location"])
            instance.location = location_new
        user_obj.full_name = validated_data["user"].get("full_name", user_obj.full_name)
        user_obj.save()
        instance.save()

        return instance


class CvSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=200)
    fileUrl = serializers.URLField(source="file_url", required=False, read_only=True)
    file = serializers.FileField(required=True, write_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Resume
        fields = ("id", "slug", "title", "fileUrl", "file")

    def update(self, instance, validated_data):
        pdf_file = validated_data.pop('file')

        pdf_upload_result = cloudinary.uploader.upload(pdf_file,
                                                       folder=settings.CLOUDINARY_DIRECTORY["cv"],
                                                       public_id=instance.id)
        pdf_public_id = pdf_upload_result.get('public_id')
        image_url = cloudinary.utils.cloudinary_url(pdf_public_id + ".jpg")[0]

        instance.file_url = pdf_upload_result["secure_url"]
        instance.image_url = image_url
        instance.public_id = pdf_public_id
        instance.save()

        return instance


class ResumeSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=200)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    salaryMin = serializers.IntegerField(source="salary_min", required=True)
    salaryMax = serializers.IntegerField(source="salary_max", required=True)
    position = serializers.IntegerField(required=True)
    experience = serializers.IntegerField(required=True)
    academicLevel = serializers.IntegerField(source="academic_level", required=True)
    typeOfWorkplace = serializers.IntegerField(source="type_of_workplace", required=True)
    jobType = serializers.IntegerField(source="job_type", required=True)
    isActive = serializers.BooleanField(source="is_active", default=False)
    updateAt = serializers.DateTimeField(source="update_at", read_only=True)
    imageUrl = serializers.URLField(source="image_url", required=False, read_only=True)
    fileUrl = serializers.URLField(source="file_url", required=False, read_only=True)
    file = serializers.FileField(required=True, write_only=True)
    user = auth_serializers.UserSerializer(fields=["id", "fullName", "avatarUrl"], read_only=True)

    isSaved = serializers.SerializerMethodField(method_name='check_saved', read_only=True)
    viewEmployerNumber = serializers.SerializerMethodField(method_name="get_view_number", read_only=True)
    userDict = auth_serializers.UserSerializer(source='user', fields=["id", "fullName"], read_only=True)
    jobSeekerProfileDict = JobSeekerProfileSerializer(source="job_seeker_profile",
                                                      fields=["id", "old"],
                                                      read_only=True)
    type = serializers.CharField(required=False, read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_fields(self, *args, **kwargs):
        fields = super(ResumeSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) in ["PUT"]:
            fields['file'].required = False
        return fields

    def get_view_number(self, resume):
        return 0

    def check_saved(self, resume):
        request = self.context.get('request', None)
        if request is None:
            return None
        user = request.user
        if user.is_authenticated and user.role_name == var_sys.EMPLOYER:
            return resume.resumesaved_set.filter(company=user.company).exists()
        return None

    class Meta:
        model = Resume
        fields = ("id", "slug", "title", "description",
                  "salaryMin", "salaryMax",
                  "position", "experience", "academicLevel",
                  "typeOfWorkplace", "jobType", "isActive",
                  "city", "career", "updateAt", "file",
                  "imageUrl", "fileUrl", "user", "city", 'isSaved',
                  "viewEmployerNumber", "userDict", "jobSeekerProfileDict",
                  "type")

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        job_seeker_profile = user.job_seeker_profile
        pdf_file = validated_data.pop('file')

        resume = Resume.objects.create(**validated_data,
                                       user=user,
                                       job_seeker_profile=job_seeker_profile)

        pdf_upload_result = cloudinary.uploader.upload(pdf_file,
                                                       folder=settings.CLOUDINARY_DIRECTORY["cv"],
                                                       public_id=resume.id)
        pdf_public_id = pdf_upload_result.get('public_id')
        image_url = cloudinary.utils.cloudinary_url(pdf_public_id + ".jpg")[0]

        resume.file_url = pdf_upload_result["secure_url"]
        resume.image_url = image_url
        resume.public_id = pdf_public_id
        resume.save()

        return resume


class ResumeViewedSerializer(serializers.ModelSerializer):
    resume = ResumeSerializer(fields=["id", "title"])
    company = CompanySerializer(fields=['id', 'slug', 'companyName', 'companyImageUrl'])
    createAt = serializers.DateTimeField(source='create_at', read_only=True)
    isSavedResume = serializers.SerializerMethodField(method_name="check_employer_save_my_resume")

    def check_employer_save_my_resume(self, resume_viewed):
        return ResumeSaved.objects.filter(
            resume=resume_viewed.resume,
            company=resume_viewed.company
        ).exists()

    class Meta:
        model = ResumeViewed
        fields = (
            'id',
            'views',
            'createAt',
            'resume',
            'company',
            'isSavedResume'
        )


class EducationSerializer(serializers.ModelSerializer):
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
    resume = serializers.SlugRelatedField(required=True, slug_field="slug", queryset=Resume.objects.all())

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def validate(self, attrs):
        if EducationDetail.objects.count() >= 10:
            raise serializers.ValidationError({'errorMessage': 'Tối đa 10 thông tin học vấn'})
        return attrs

    class Meta:
        model = EducationDetail
        fields = ('id', 'degreeName', 'major', 'trainingPlaceName',
                  'startDate', 'completedDate', 'description', 'resume')


class ExperienceSerializer(serializers.ModelSerializer):
    jobName = serializers.CharField(source='job_name', required=True, max_length=200)
    companyName = serializers.CharField(source='company_name', required=True, max_length=255)
    startDate = serializers.DateField(source='start_date', required=True,
                                      input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                     var_sys.DATE_TIME_FORMAT["Ymd"]])
    endDate = serializers.DateField(source='end_date', required=True,
                                    input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                   var_sys.DATE_TIME_FORMAT["Ymd"]])
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    resume = serializers.SlugRelatedField(required=True, slug_field="slug", queryset=Resume.objects.all())

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def validate(self, attrs):
        if ExperienceDetail.objects.count() >= 10:
            raise serializers.ValidationError({'errorMessage': 'Tối đa 10 thông tin kinh nghiệm làm việc'})
        return attrs

    class Meta:
        model = ExperienceDetail
        fields = ('id', 'jobName', 'companyName',
                  'startDate', 'endDate',
                  'description', 'resume')


class CertificateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200)
    trainingPlace = serializers.CharField(source='training_place', required=True, max_length=255)
    startDate = serializers.DateField(source='start_date', required=True,
                                      input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                     var_sys.DATE_TIME_FORMAT["Ymd"]])
    expirationDate = serializers.DateField(source='expiration_date', required=False, allow_null=True,
                                           input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                          var_sys.DATE_TIME_FORMAT["Ymd"]])
    resume = serializers.SlugRelatedField(required=True, slug_field="slug", queryset=Resume.objects.all())

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def validate(self, attrs):
        if Certificate.objects.count() >= 10:
            raise serializers.ValidationError({'errorMessage': 'Tối đa 10 thông tin chứng chỉ'})
        return attrs

    class Meta:
        model = Certificate
        fields = ('id', 'name', 'trainingPlace', 'startDate',
                  'expirationDate', 'resume')


class LanguageSkillSerializer(serializers.ModelSerializer):
    language = serializers.IntegerField(required=True)
    level = serializers.IntegerField(required=True)
    resume = serializers.SlugRelatedField(required=True, slug_field="slug", queryset=Resume.objects.all())

    # def validate_language(self, language):
    #     request = self.context['request']
    #
    #     if LanguageSkill.objects.filter(language=language,
    #                                     # job_seeker_profile=request.user.job_seeker_profile
    #                                     ).exists():
    #         raise serializers.ValidationError('Ngôn ngữ này đã tồn tại.')
    #     return language

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = LanguageSkill
        fields = ('id', 'language', 'level', 'resume')


class AdvancedSkillSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200)
    level = serializers.IntegerField(required=True)
    resume = serializers.SlugRelatedField(required=True, slug_field="slug", queryset=Resume.objects.all())

    # def validate_name(self, name):
    #     request = self.context['request']
    #
    #     if AdvancedSkill.objects.filter(name__iexact=name,
    #                                     # job_seeker_profile=request.user.job_seeker_profile
    #                                     ).exists():
    #         raise serializers.ValidationError('Kỹ năng này đã tồn tại.')
    #     return name

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def validate(self, attrs):
        if AdvancedSkill.objects.count() >= 15:
            raise serializers.ValidationError({'errorMessage': 'Tối đa 15 thông tin kỹ năng chuyên môn'})
        return attrs

    class Meta:
        model = AdvancedSkill
        fields = ('id', 'name', 'level', 'resume')


class ResumeDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=200)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    salaryMin = serializers.IntegerField(source="salary_min", required=True)
    salaryMax = serializers.IntegerField(source="salary_max", required=True)
    position = serializers.IntegerField(required=True)
    experience = serializers.IntegerField(required=True)
    academicLevel = serializers.IntegerField(source="academic_level", required=True)
    typeOfWorkplace = serializers.IntegerField(source="type_of_workplace", required=True)
    jobType = serializers.IntegerField(source="job_type", required=True)
    isActive = serializers.BooleanField(source="is_active", default=False)
    updateAt = serializers.DateTimeField(source="update_at", read_only=True)
    fileUrl = serializers.URLField(source="file_url", required=False, read_only=True)
    filePublicId = serializers.CharField(source="public_id", read_only=True)
    type = serializers.CharField(required=False, read_only=True)

    isSaved = serializers.SerializerMethodField(method_name='check_saved', read_only=True)
    user = auth_serializers.UserSerializer(fields=["id", "fullName", "email", "avatarUrl"],
                                           read_only=True)
    jobSeekerProfile = JobSeekerProfileSerializer(source="job_seeker_profile",
                                                  fields=[
                                                      "id", "phone", "birthday",
                                                      "gender", "maritalStatus", "location"
                                                  ],
                                                  read_only=True)
    experiencesDetails = ExperienceSerializer(source="experience_details",
                                              fields=[
                                                  'id', 'jobName', 'companyName',
                                                  'startDate', 'endDate',
                                                  'description',
                                              ],
                                              read_only=True, many=True)
    educationDetails = EducationSerializer(source="education_details",
                                           fields=[
                                               'id', 'degreeName', 'major', 'trainingPlaceName',
                                               'startDate', 'completedDate', 'description'
                                           ], read_only=True, many=True)
    certificates = CertificateSerializer(fields=[
        'id', 'name', 'trainingPlace', 'startDate',
        'expirationDate'
    ], read_only=True, many=True)
    languageSkills = LanguageSkillSerializer(source="language_skills",
                                             fields=[
                                                 'id', 'language', 'level'
                                             ], read_only=True, many=True)
    advancedSkills = AdvancedSkillSerializer(source="advanced_skills",
                                             fields=[
                                                 'id', 'name', 'level'
                                             ],
                                             read_only=True, many=True)

    def check_saved(self, resume):
        request = self.context.get('request', None)
        if request is None:
            return None
        user = request.user
        if user.is_authenticated and user.role_name == var_sys.EMPLOYER:
            return resume.resumesaved_set.filter(company=user.company).exists()
        return None

    class Meta:
        model = Resume
        fields = ("id", "slug", "title", "description",
                  "salaryMin", "salaryMax",
                  "position", "experience", "academicLevel",
                  "typeOfWorkplace", "jobType", "isActive",
                  "city", "career", "updateAt", "fileUrl",
                  "filePublicId", "city", 'isSaved', "type",
                  "user", "jobSeekerProfile",
                  "experiencesDetails", "educationDetails",
                  "certificates", "languageSkills", "advancedSkills"
                  )

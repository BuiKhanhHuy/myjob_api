"""
MyJob Recruitment System - Part of MyJob Platform

Author: Bui Khanh Huy
Email: khuy220@gmail.com
Copyright (c) 2023 Bui Khanh Huy

License: MIT License
See the LICENSE file in the project root for full license information.
"""

import datetime
from datetime import date
from django.conf import settings
from configs import variable_system as var_sys
from configs.messages import ERROR_MESSAGES
from helpers import helper
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.db import transaction
from console.jobs import queue_auth
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
    Location, File
)

from authentication import serializers as auth_serializers
from common import serializers as common_serializers
from helpers.cloudinary_service import CloudinaryService


class CompanyImageSerializer(serializers.ModelSerializer):
    imageUrl = serializers.SerializerMethodField(
        method_name='get_image_url', read_only=True)
    files = serializers.ListField(required=True, write_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_image_url(self, company_image):
        if company_image.image:
            return company_image.image.get_full_url()

        return None

    def validate(self, attrs):
        files = attrs.get("files", [])
        count_upload_file = len(files)

        request = self.context['request']
        user = request.user
        if user.role_name == var_sys.EMPLOYER:
            company = user.company
            if CompanyImage.objects.filter(company=company).count() + count_upload_file > 15:
                raise serializers.ValidationError(
                    {'errorMessage': ERROR_MESSAGES["MAXIMUM_IMAGES"]})
        return attrs

    def create(self, validated_data):
        # Extract the 'files' field from the validated data
        files = validated_data.pop('files', [])
        # Get the request from the context
        request = self.context["request"]

        # Initialize an empty list to store the file names
        file_name_list = []
        # Start a database transaction
        with transaction.atomic():
            # Loop through each file in the 'files' list
            for file in files:
                # Create a new CompanyImage object for the current user's company
                company_image = CompanyImage.objects.create(
                    company=request.user.company)
                # Upload the file to Cloudinary
                company_image_upload_result = CloudinaryService.upload_image(
                    file,
                    settings.CLOUDINARY_DIRECTORY["company_image"]
                )
                # Create file
                image = File.update_or_create_file_with_cloudinary(
                    None,
                    company_image_upload_result,
                    File.COMPANY_IMAGE_TYPE
                )
                # Set the image of the CompanyImage object to the uploaded image
                company_image.image = image
                # Save the CompanyImage object
                company_image.save()

                # Add the file name and URL to the list
                file_name_list.append({
                    'id': company_image.id,
                    'imageUrl': company_image.image.get_full_url() if company_image.image else None
                })

        # Return the list of file names and URLs
        return file_name_list

    class Meta:
        model = CompanyImage
        fields = ('id', 'imageUrl', 'files')


class CompanySerializer(serializers.ModelSerializer):
    taxCode = serializers.CharField(source="tax_code", required=True, max_length=30,
                                    validators=[UniqueValidator(Company.objects.all(),
                                                                message=ERROR_MESSAGES["COMPANY_TAX_CODE_EXISTS"])])
    companyName = serializers.CharField(source="company_name", required=True,
                                        validators=[UniqueValidator(Company.objects.all(),
                                                                    message=ERROR_MESSAGES["COMPANY_NAME_EXISTS"])])
    employeeSize = serializers.IntegerField(
        source="employee_size", required=True)
    fieldOperation = serializers.CharField(source="field_operation", required=True,
                                           max_length=255)
    location = common_serializers.LocationSerializer()
    since = serializers.DateField(required=True, allow_null=True, input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                                                 var_sys.DATE_TIME_FORMAT["Ymd"]])
    companyEmail = serializers.CharField(source="company_email", required=True,
                                         max_length=100, validators=[UniqueValidator(Company.objects.all(),
                                                                                     message=ERROR_MESSAGES["COMPANY_EMAIL_EXISTS"])])
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
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True)

    companyImageUrl = serializers.SerializerMethodField(
        method_name='get_company_logo_url', read_only=True)
    companyCoverImageUrl = serializers.SerializerMethodField(
        method_name='get_company_cover_image_url', read_only=True)
    locationDict = common_serializers.LocationSerializer(source="location",
                                                         fields=['city'],
                                                         read_only=True)

    followNumber = serializers.SerializerMethodField(
        method_name="get_follow_number", read_only=True)
    jobPostNumber = serializers.SerializerMethodField(
        method_name="get_job_post_number", read_only=True)
    isFollowed = serializers.SerializerMethodField(
        method_name='check_followed', read_only=True)
    companyImages = CompanyImageSerializer(source='company_images', many=True, read_only=True,
                                           fields=['id', 'imageUrl'])

    mobileUserDict = auth_serializers.UserSerializer(source='user', read_only=True,
                                                     fields=["id", "fullName", "email"])

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_company_logo_url(self, company):
        logo = company.logo
        if logo:
            return logo.get_full_url()

        return var_sys.AVATAR_DEFAULT["COMPANY_LOGO"]

    def get_company_cover_image_url(self, company):
        cover_image = company.cover_image
        if cover_image:
            return cover_image.get_full_url()

        return var_sys.AVATAR_DEFAULT["COMPANY_COVER_IMAGE"]

    def get_follow_number(self, company):
        return company.companyfollowed_set.filter().count()

    def get_job_post_number(self, company):
        now = datetime.datetime.now().date()
        return company.job_posts.filter(deadline__gte=now, status=var_sys.JOB_POST_STATUS[2][0]).count()

    def check_followed(self, company):
        request = self.context.get('request', None)
        if request is None:
            return False
        user = request.user
        if user.is_authenticated:
            return company.companyfollowed_set.filter(user=user).count() > 0
        return False

    class Meta:
        model = Company
        fields = ('id', 'slug', 'taxCode', 'companyName',
                  'employeeSize', 'fieldOperation', 'location',
                  'since', 'companyEmail', 'companyPhone',
                  'websiteUrl', 'facebookUrl', 'youtubeUrl', 'linkedinUrl',
                  'description',
                  'companyImageUrl', 'companyCoverImageUrl', 'locationDict',
                  'followNumber', 'jobPostNumber', 'isFollowed',
                  'companyImages', 'mobileUserDict')

    def update(self, instance, validated_data):
        try:
            instance.tax_code = validated_data.get(
                'tax_code', instance.tax_code)
            instance.company_name = validated_data.get(
                'company_name', instance.company_name)
            instance.employee_size = validated_data.get(
                'employee_size', instance.employee_size)
            instance.field_operation = validated_data.get(
                'field_operation', instance.field_operation)
            instance.since = validated_data.get('since', instance.since)
            instance.company_email = validated_data.get(
                'company_email', instance.company_email)
            instance.company_phone = validated_data.get(
                'company_phone', instance.company_phone)
            instance.website_url = validated_data.get(
                'website_url', instance.website_url)
            instance.facebook_url = validated_data.get(
                'facebook_url', instance.facebook_url)
            instance.youtube_url = validated_data.get(
                'youtube_url', instance.youtube_url)
            instance.linkedin_url = validated_data.get(
                'linkedin_url', instance.linkedin_url)
            instance.description = validated_data.get(
                'description', instance.description)
            location_obj = instance.location

            with transaction.atomic():
                if location_obj:
                    location_obj.city = validated_data["location"].get(
                        "city", location_obj.city)
                    location_obj.district = validated_data["location"].get(
                        "district", location_obj.district)
                    location_obj.address = validated_data["location"].get(
                        "address", location_obj.address)
                    location_obj.lat = validated_data["location"].get(
                        "lat", location_obj.lat)
                    location_obj.lng = validated_data["location"].get(
                        "lng", location_obj.lng)
                    location_obj.save()
                else:
                    location_new = Location.objects.create(
                        **validated_data["location"])
                    instance.location = location_new
                instance.save()

                # update in firebase
                queue_auth.update_info.delay(
                    instance.user_id, instance.company_name)

                return instance
        except Exception as ex:
            helper.print_log_error("update company", ex)
            return None


class CompanyFollowedSerializer(serializers.ModelSerializer):
    company = CompanySerializer(fields=['id', 'slug', 'companyName', 'companyImageUrl',
                                        'fieldOperation', 'followNumber', 'jobPostNumber',
                                        'isFollowed'])

    class Meta:
        model = CompanyFollowed
        fields = (
            'id',
            'company',
        )


class LogoCompanySerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True, write_only=True)
    companyImageUrl = serializers.SerializerMethodField(
        method_name='get_company_logo_url', read_only=True)

    class Meta:
        model = Company
        fields = ('file', 'companyImageUrl')

    def get_company_logo_url(self, company):
        logo = company.logo
        if logo:
            return logo.get_full_url()

        return var_sys.AVATAR_DEFAULT["COMPANY_LOGO"]

    def update(self, company, validated_data):
        file = validated_data.pop('file')

        try:
            with transaction.atomic():
                public_id = None
                # Overwrite if image already exists
                if company.logo:
                    path_list = company.logo.public_id.split('/')
                    public_id = path_list[-1] if path_list else None
                # Upload the logo to Cloudinary
                logo_upload_result = CloudinaryService.upload_image(
                    file,
                    settings.CLOUDINARY_DIRECTORY["logo"],
                    public_id=public_id
                )
                # Update or create file
                company.logo = File.update_or_create_file_with_cloudinary(
                    company.logo,
                    logo_upload_result,
                    File.LOGO_TYPE
                )
                company.save()

                # Update the company avatar in Firebase
                queue_auth.update_avatar.delay(
                    company.user_id, company.logo.get_full_url())

            return company
        except Exception as e:
            # Log the error if any occurs during the process
            helper.print_log_error("update company logo", e)
            return None


class CompanyCoverImageSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True, write_only=True)
    companyCoverImageUrl = serializers.SerializerMethodField(
        method_name='get_company_cover_image_url', read_only=True)

    class Meta:
        model = Company
        fields = ('file', 'companyCoverImageUrl')

    def get_company_cover_image_url(self, company):
        cover_image = company.cover_image
        if cover_image:
            return cover_image.get_full_url()

        return var_sys.AVATAR_DEFAULT["COMPANY_COVER_IMAGE"]

    def update(self, company, validated_data):
        file = validated_data.pop('file')

        try:
            with transaction.atomic():
                public_id = None
                # Overwrite if image already exists
                if company.cover_image:
                    path_list = company.cover_image.public_id.split('/')
                    public_id = path_list[-1] if path_list else None
                # Upload the company cover image to Cloudinary
                company_cover_image_upload_result = CloudinaryService.upload_image(
                    file,
                    settings.CLOUDINARY_DIRECTORY["cover_image"],
                    public_id=public_id
                )
                # Update or create file
                company.cover_image = File.update_or_create_file_with_cloudinary(
                    company.cover_image,
                    company_cover_image_upload_result,
                    File.COVER_IMAGE_TYPE
                )
                company.save()
            return company
        except:
            return None


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True, max_length=15)
    birthday = serializers.DateField(required=True,
                                     input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                    var_sys.DATE_TIME_FORMAT["Ymd"]])
    gender = serializers.CharField(required=True, max_length=1)
    maritalStatus = serializers.CharField(source='marital_status',
                                          required=True,
                                          max_length=1)
    location = common_serializers.ProfileLocationSerializer()
    user = auth_serializers.UserSerializer(fields=["fullName"])
    old = serializers.SerializerMethodField(
        method_name="get_old", read_only=True)

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
            age = today.year - birthdate.year - \
                ((today.month, today.day) < (birthdate.month, birthdate.day))
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
        instance.marital_status = validated_data.get(
            'marital_status', instance.marital_status)
        location_obj = instance.location
        user_obj = instance.user

        if location_obj:
            location_obj.city = validated_data["location"].get(
                "city", location_obj.city)
            location_obj.district = validated_data["location"].get(
                "district", location_obj.district)
            location_obj.address = validated_data["location"].get(
                "address", location_obj.address)
            location_obj.save()
        else:
            location_new = Location.objects.create(
                **validated_data["location"])
            instance.location = location_new
        user_obj.full_name = validated_data["user"].get(
            "full_name", user_obj.full_name)
        user_obj.save()

        # update in firebase
        queue_auth.update_info.delay(user_obj.id, user_obj.full_name)

        instance.save()
        return instance


class CvSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=200)
    fileUrl = serializers.SerializerMethodField(
        method_name="get_cv_file_url", read_only=True)
    file = serializers.FileField(required=True, write_only=True)

    updateAt = serializers.DateTimeField(source='update_at', read_only=True)

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
        fields = ("id", "slug", "title", "fileUrl", "file", "updateAt")

    def get_cv_file_url(self, resume):
        cv_file = resume.file
        if cv_file:
            return cv_file.get_full_url()
        return None

    def update(self, instance, validated_data):
        # Extract the PDF file from validated data
        pdf_file = validated_data.pop('file')

        public_id = None
        # Overwrite if image already exists
        if instance.file:
            path_list = instance.file.public_id.split('/')
            public_id = path_list[-1] if path_list else None
        # Upload the PDF file to Cloudinary
        pdf_upload_result = CloudinaryService.upload_file(
            pdf_file,
            settings.CLOUDINARY_DIRECTORY["cv"],
            public_id=public_id
        )
        # Update or create file
        instance.file = File.update_or_create_file_with_cloudinary(
            instance.file,
            pdf_upload_result,
            File.CV_TYPE
        )
        # Save the instance to ensure any other changes are persisted
        instance.save()

        return instance


class ResumeSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=200)
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    salaryMin = serializers.IntegerField(source="salary_min", required=True)
    salaryMax = serializers.IntegerField(source="salary_max", required=True)
    position = serializers.IntegerField(required=True)
    positionChooseData = serializers.SerializerMethodField(
        method_name="get_position_data", read_only=True)
    experience = serializers.IntegerField(required=True)
    experienceChooseData = serializers.SerializerMethodField(
        method_name="get_experience_data", read_only=True)
    academicLevel = serializers.IntegerField(
        source="academic_level", required=True)
    academicLevelChooseData = serializers.SerializerMethodField(
        method_name="get_academic_level_data", read_only=True)
    typeOfWorkplace = serializers.IntegerField(
        source="type_of_workplace", required=True)
    typeOfWorkplaceChooseData = serializers.SerializerMethodField(
        method_name="get_type_of_workplace_data", read_only=True)
    jobType = serializers.IntegerField(source="job_type", required=True)
    jobTypeChooseData = serializers.SerializerMethodField(
        method_name="get_job_type_data", read_only=True)
    isActive = serializers.BooleanField(source="is_active", default=False)
    updateAt = serializers.DateTimeField(source="update_at", read_only=True)
    imageUrl = serializers.SerializerMethodField(
        method_name="get_cv_image_url", read_only=True)
    fileUrl = serializers.SerializerMethodField(
        method_name="get_cv_file_url", read_only=True)
    file = serializers.FileField(required=True, write_only=True)
    user = auth_serializers.UserSerializer(
        fields=["id", "fullName", "avatarUrl"], read_only=True)

    isSaved = serializers.SerializerMethodField(
        method_name='check_saved', read_only=True)
    viewEmployerNumber = serializers.SerializerMethodField(
        method_name="get_view_number", read_only=True)
    userDict = auth_serializers.UserSerializer(
        source='user', fields=["id", "fullName"], read_only=True)
    jobSeekerProfileDict = JobSeekerProfileSerializer(source="job_seeker_profile",
                                                      fields=["id", "old"],
                                                      read_only=True)
    lastViewedDate = serializers.SerializerMethodField(
        method_name='get_last_viewed_date', read_only=True)
    type = serializers.CharField(required=False, read_only=True)
    experienceDetails = serializers.SerializerMethodField(
        method_name="get_experience_details", read_only=True)
    educationDetails = serializers.SerializerMethodField(
        method_name="get_education_details", read_only=True)
    certificateDetails = serializers.SerializerMethodField(
        method_name="get_certificate_details", read_only=True)
    languageSkills = serializers.SerializerMethodField(
        method_name="get_language_skills", read_only=True)
    advancedSkills = serializers.SerializerMethodField(
        method_name="get_advanced_skills", read_only=True)

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
        return resume.resumesaved_set.count()

    def check_saved(self, resume):
        request = self.context.get('request', None)
        if request is None:
            return None
        user = request.user
        if user.is_authenticated and user.role_name == var_sys.EMPLOYER:
            return resume.resumesaved_set.filter(company=user.company).exists()
        return None

    def get_last_viewed_date(self, resume):
        request = self.context.get('request', None)
        if request is None:
            return None
        company = request.user.company
        if not company:
            return None
        resume_viewed = ResumeViewed.objects.filter(
            company=company, resume=resume).first()
        if not resume_viewed:
            return None

        return resume_viewed.update_at

    def get_cv_image_url(self, resume):
        cv_file = resume.file
        if cv_file:
            return cv_file.get_full_url().replace(f".{cv_file.format}", ".jpg")
        return None

    def get_cv_file_url(self, resume):
        cv_file = resume.file
        if cv_file:
            return cv_file.get_full_url()
        return None

    def get_position_data(self, resume):
        if resume.position is not None:
            return {
                'id': resume.position,
                'name': resume.get_position_display()
            }
        return None

    def get_experience_data(self, resume):
        if resume.experience is not None:
            return {
                'id': resume.experience,
                'name': resume.get_experience_display()
            }
        return None

    def get_academic_level_data(self, resume):
        if resume.academic_level is not None:
            return {
                'id': resume.academic_level,
                'name': resume.get_academic_level_display()
            }
        return None

    def get_type_of_workplace_data(self, resume):
        if resume.type_of_workplace is not None:
            return {
                'id': resume.type_of_workplace,
                'name': resume.get_type_of_workplace_display()
            }
        return None

    def get_job_type_data(self, resume):
        if resume.job_type is not None:
            return {
                'id': resume.job_type,
                'name': resume.get_job_type_display()
            }
        return None

    def get_experience_details(self, resume):
        experiences = []
        for exp in resume.experience_details.all():
            experiences.append({
                'id': exp.id,
                'jobName': exp.job_name,
                'companyName': exp.company_name,
                'startDate': exp.start_date.isoformat() if exp.start_date else None,
                'endDate': exp.end_date.isoformat() if exp.end_date else None,
                'description': exp.description
            })
        return experiences

    def get_education_details(self, resume):
        educations = []
        for edu in resume.education_details.all():
            educations.append({
                'id': edu.id,
                'degreeName': edu.degree_name,
                'major': edu.major,
                'trainingPlaceName': edu.training_place_name,
                'startDate': edu.start_date.isoformat() if edu.start_date else None,
                'completedDate': edu.completed_date.isoformat() if edu.completed_date else None,
                'description': edu.description
            })
        return educations

    def get_certificate_details(self, resume):
        certificates = []
        for cert in resume.certificates.all():
            certificates.append({
                'id': cert.id,
                'name': cert.name,
                'trainingPlace': cert.training_place,
                'startDate': cert.start_date.isoformat() if cert.start_date else None,
                'expirationDate': cert.expiration_date.isoformat() if cert.expiration_date else None
            })
        return certificates

    def get_language_skills(self, resume):
        languages = []
        for lang in resume.language_skills.all():
            languages.append({
                'id': lang.id,
                'language': lang.get_language_display() if lang.language else None,
                'level': lang.level
            })
        return languages

    def get_advanced_skills(self, resume):
        skills = []
        for skill in resume.advanced_skills.all():
            skills.append({
                'id': skill.id,
                'name': skill.name,
                'level': skill.level
            })
        return skills

    class Meta:
        model = Resume
        fields = ("id", "slug", "title", "description",
                  "salaryMin", "salaryMax",
                  "position", "experience", "academicLevel",
                  "typeOfWorkplace", "jobType", "isActive",
                  "career", "updateAt", "file",
                  "imageUrl", "fileUrl", "user", "city", 'isSaved',
                  "viewEmployerNumber", "lastViewedDate",
                  "userDict", "jobSeekerProfileDict",
                  "type", "positionChooseData", "experienceChooseData", "academicLevelChooseData",
                  "typeOfWorkplaceChooseData", "jobTypeChooseData",
                  "experienceDetails", "educationDetails", "certificateDetails",
                  "languageSkills", "advancedSkills")

    def create(self, validated_data):
        with transaction.atomic():
            # Retrieve the request and user from the serializer context
            request = self.context['request']
            user = request.user
            # Get the job seeker profile associated with the user
            job_seeker_profile = user.job_seeker_profile
            # Remove the 'file' field from validated_data as it's handled separately
            pdf_file = validated_data.pop('file')

            # Create a new Resume instance with the validated data and additional fields
            resume = Resume.objects.create(**validated_data,
                                           user=user,
                                           job_seeker_profile=job_seeker_profile)

            # Upload the PDF file to Cloudinary and get the upload result
            pdf_upload_result = CloudinaryService.upload_file(
                pdf_file,
                settings.CLOUDINARY_DIRECTORY["cv"]
            )
            # Update or create file
            resume.file = File.update_or_create_file_with_cloudinary(
                resume.file,
                pdf_upload_result,
                File.CV_TYPE
            )
            # Save the resume instance to reflect the changes
            resume.save()

            # Return the newly created resume instance
            return resume


class ExperiencePdfSerializer(serializers.ModelSerializer):
    jobName = serializers.CharField(source='job_name', read_only=True)
    companyName = serializers.CharField(source='company_name', read_only=True)
    startDate = serializers.DateField(source='start_date', read_only=True)
    endDate = serializers.DateField(source='end_date', read_only=True)
    description = serializers.CharField(read_only=True)

    class Meta:
        model = ExperienceDetail
        fields = ('id', 'jobName', 'companyName',
                  'startDate', 'endDate',
                  'description')


class EducationPdfSerializer(serializers.ModelSerializer):
    degreeName = serializers.CharField(source='degree_name', read_only=True)
    major = serializers.CharField(read_only=True)
    trainingPlaceName = serializers.CharField(
        source='training_place_name', read_only=True)
    startDate = serializers.DateField(source='start_date', read_only=True)
    completedDate = serializers.DateField(
        source='completed_date', read_only=True)
    description = serializers.CharField(read_only=True)

    class Meta:
        model = EducationDetail
        fields = ('id', 'degreeName', 'major', 'trainingPlaceName',
                  'startDate', 'completedDate', 'description')


class CertificatePdfSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    trainingPlace = serializers.CharField(
        source='training_place', read_only=True)
    startDate = serializers.DateField(source='start_date', read_only=True)
    expirationDate = serializers.DateField(read_only=True)

    class Meta:
        model = Certificate
        fields = ('id', 'name', 'trainingPlace',
                  'startDate',
                  'expirationDate')


class LanguageSkillPdfSerializer(serializers.ModelSerializer):
    language = serializers.IntegerField(read_only=True)
    level = serializers.IntegerField(read_only=True)

    class Meta:
        model = LanguageSkill
        fields = ('id', 'language', 'level')


class AdvancedSkillPdfSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    level = serializers.IntegerField(read_only=True)

    class Meta:
        model = AdvancedSkill
        fields = ('id', 'name', 'level')


class ResumePdfViewSerializer(serializers.ModelSerializer):
    title = serializers.CharField(read_only=True, )
    description = serializers.CharField(read_only=True, )
    salaryMin = serializers.IntegerField(source="salary_min", read_only=True, )
    salaryMax = serializers.IntegerField(source="salary_max", read_only=True, )
    experience = serializers.IntegerField(read_only=True, )
    academicLevel = serializers.IntegerField(
        source="academic_level", read_only=True, )
    typeOfWorkplace = serializers.IntegerField(
        source="type_of_workplace", read_only=True, )
    jobType = serializers.IntegerField(source="job_type", read_only=True, )
    user = auth_serializers.UserSerializer(read_only=True, fields=[
        "fullName",
        "avatarUrl",
        "email"
    ])
    jobSeekerProfile = JobSeekerProfileSerializer(source='job_seeker_profile', read_only=True, fields=[
        "phone",
        "birthday",
    ])
    experienceDetails = ExperiencePdfSerializer(
        source='experience_details', read_only=True, many=True)
    educationDetails = EducationPdfSerializer(
        source='education_details', read_only=True, many=True)
    certificates = CertificatePdfSerializer(read_only=True, many=True)
    languageSkills = LanguageSkillPdfSerializer(
        source='language_skills', read_only=True, many=True)
    advancedSkills = AdvancedSkillPdfSerializer(
        source='advanced_skills', read_only=True, many=True)

    class Meta:
        model = Resume
        fields = ("title", "description",
                  "salaryMin", "salaryMax",
                  "position", "experience",
                  "academicLevel",
                  "typeOfWorkplace", "jobType",
                  "career", "user", "city",
                  "user",
                  "jobSeekerProfile",
                  "experienceDetails",
                  "educationDetails",
                  "certificates",
                  "languageSkills",
                  "advancedSkills"
                  )


class ResumeViewedSerializer(serializers.ModelSerializer):
    resume = ResumeSerializer(fields=["id", "title"])
    company = CompanySerializer(
        fields=['id', 'slug', 'companyName', 'companyImageUrl'])
    createAt = serializers.DateTimeField(source='create_at', read_only=True)
    isSavedResume = serializers.SerializerMethodField(
        method_name="check_employer_save_my_resume")

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


class ResumeSavedSerializer(serializers.ModelSerializer):
    resume = ResumeSerializer(fields=[
        "id", "slug", "title", "salaryMin", "salaryMax",
        "experience", "city", "userDict", "jobSeekerProfileDict", "type"
    ])
    createAt = serializers.DateTimeField(source='create_at', read_only=True)
    updateAt = serializers.DateTimeField(source='update_at', read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = ResumeSaved
        fields = ("id", "resume", "createAt", "updateAt")


class ResumeSavedExportSerializer(serializers.ModelSerializer):
    title = serializers.PrimaryKeyRelatedField(
        source="resume.title", read_only=True)
    fullName = serializers.PrimaryKeyRelatedField(
        source="resume.user.full_name", read_only=True)
    email = serializers.PrimaryKeyRelatedField(
        source="resume.user.email", read_only=True)
    phone = serializers.PrimaryKeyRelatedField(
        source="resume.job_seeker_profile.phone", read_only=True)
    gender = serializers.PrimaryKeyRelatedField(
        source="resume.job_seeker_profile.gender", read_only=True)

    birthday = serializers.PrimaryKeyRelatedField(
        source="resume.job_seeker_profile.birthday", read_only=True)
    address = serializers.PrimaryKeyRelatedField(
        source="resume.job_seeker_profile.location.city.name", read_only=True)
    createAt = serializers.DateTimeField(source='create_at', read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = ResumeSaved
        fields = ("title", "fullName", "email", "phone",
                  "gender", "birthday", "address",
                  "createAt")


class EducationSerializer(serializers.ModelSerializer):
    degreeName = serializers.CharField(
        source='degree_name', required=True, max_length=200)
    major = serializers.CharField(required=True, max_length=255)
    trainingPlaceName = serializers.CharField(
        source='training_place_name', required=True, max_length=255)
    startDate = serializers.DateField(source='start_date', required=True,
                                      input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                     var_sys.DATE_TIME_FORMAT["Ymd"]])
    completedDate = serializers.DateField(source='completed_date', required=False, allow_null=True,
                                          input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                         var_sys.DATE_TIME_FORMAT["Ymd"]])
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)

    # slug field for web
    resume = serializers.SlugRelatedField(
        required=False, slug_field="slug", queryset=Resume.objects.all())
    # primary key field for app
    resumeId = serializers.PrimaryKeyRelatedField(
        source='resume',
        queryset=Resume.objects.all(),
        required=False
    )

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
            raise serializers.ValidationError(
                {'errorMessage': ERROR_MESSAGES["MAXIMUM_EDUCATION"]})
        return attrs

    class Meta:
        model = EducationDetail
        fields = ('id', 'degreeName', 'major', 'trainingPlaceName',
                  'startDate', 'completedDate', 'description', 'resume', 'resumeId')


class ExperienceSerializer(serializers.ModelSerializer):
    jobName = serializers.CharField(
        source='job_name', required=True, max_length=200)
    companyName = serializers.CharField(
        source='company_name', required=True, max_length=255)
    startDate = serializers.DateField(source='start_date', required=True,
                                      input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                     var_sys.DATE_TIME_FORMAT["Ymd"]])
    endDate = serializers.DateField(source='end_date', required=True,
                                    input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                   var_sys.DATE_TIME_FORMAT["Ymd"]])
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)

    # slug field for web
    resume = serializers.SlugRelatedField(
        required=False, slug_field="slug", queryset=Resume.objects.all())
    # primary key field for app
    resumeId = serializers.PrimaryKeyRelatedField(
        source='resume',
        queryset=Resume.objects.all(),
        required=False
    )

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
            raise serializers.ValidationError(
                {'errorMessage': ERROR_MESSAGES["MAXIMUM_EXPERIENCE"]})
        return attrs

    class Meta:
        model = ExperienceDetail
        fields = ('id', 'jobName', 'companyName',
                  'startDate', 'endDate',
                  'description', 'resume', 'resumeId')


class CertificateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200)
    trainingPlace = serializers.CharField(
        source='training_place', required=True, max_length=255)
    startDate = serializers.DateField(source='start_date', required=True,
                                      input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                     var_sys.DATE_TIME_FORMAT["Ymd"]])
    expirationDate = serializers.DateField(source='expiration_date', required=False, allow_null=True,
                                           input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                          var_sys.DATE_TIME_FORMAT["Ymd"]])

    # slug field for web
    resume = serializers.SlugRelatedField(
        required=False, slug_field="slug", queryset=Resume.objects.all())
    # primary key field for app
    resumeId = serializers.PrimaryKeyRelatedField(
        source='resume',
        queryset=Resume.objects.all(),
        required=False
    )

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
            raise serializers.ValidationError(
                {'errorMessage': ERROR_MESSAGES["MAXIMUM_CERTIFICATE"]})
        return attrs

    class Meta:
        model = Certificate
        fields = ('id', 'name', 'trainingPlace', 'startDate',
                  'expirationDate', 'resume', 'resumeId')


class LanguageSkillSerializer(serializers.ModelSerializer):
    language = serializers.IntegerField(required=True)
    level = serializers.IntegerField(required=True)

    # slug field for web
    resume = serializers.SlugRelatedField(
        required=False, slug_field="slug", queryset=Resume.objects.all())
    # primary key field for app
    resumeId = serializers.PrimaryKeyRelatedField(
        source='resume',
        queryset=Resume.objects.all(),
        required=False
    )

    # TODO:
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
        fields = ('id', 'language', 'level', 'resume', 'resumeId')


class AdvancedSkillSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200)
    level = serializers.IntegerField(required=True)

    # slug field for web
    resume = serializers.SlugRelatedField(
        required=False, slug_field="slug", queryset=Resume.objects.all())
    # primary key field for app
    resumeId = serializers.PrimaryKeyRelatedField(
        source='resume',
        queryset=Resume.objects.all(),
        required=False
    )

    # TODO:
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
            raise serializers.ValidationError(
                {'errorMessage': ERROR_MESSAGES["MAXIMUM_ADVANCED"]})
        return attrs

    class Meta:
        model = AdvancedSkill
        fields = ('id', 'name', 'level', 'resume', "resumeId")


class ResumeDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=200)
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    salaryMin = serializers.IntegerField(source="salary_min", required=True)
    salaryMax = serializers.IntegerField(source="salary_max", required=True)
    position = serializers.IntegerField(required=True)
    experience = serializers.IntegerField(required=True)
    academicLevel = serializers.IntegerField(
        source="academic_level", required=True)
    typeOfWorkplace = serializers.IntegerField(
        source="type_of_workplace", required=True)
    jobType = serializers.IntegerField(source="job_type", required=True)
    isActive = serializers.BooleanField(source="is_active", default=False)
    updateAt = serializers.DateTimeField(source="update_at", read_only=True)
    fileUrl = serializers.URLField(
        source="file_url", required=False, read_only=True)
    filePublicId = serializers.CharField(source="public_id", read_only=True)
    type = serializers.CharField(required=False, read_only=True)

    isSaved = serializers.SerializerMethodField(
        method_name='check_saved', read_only=True)
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
    lastViewedDate = serializers.SerializerMethodField(
        method_name='get_last_viewed_date', read_only=True)
    isSentEmail = serializers.SerializerMethodField(
        method_name='check_sent_email', read_only=True)

    def check_saved(self, resume):
        request = self.context.get('request', None)
        if request is None:
            return None
        user = request.user
        if user.is_authenticated and user.role_name == var_sys.EMPLOYER:
            return resume.resumesaved_set.filter(company=user.company).exists()
        return None

    def get_last_viewed_date(self, resume):
        request = self.context.get('request', None)
        if request is None:
            return None
        company = request.user.company
        if not company:
            return None
        resume_viewed = ResumeViewed.objects.filter(
            company=company, resume=resume).first()
        if not resume_viewed:
            return None

        return resume_viewed.update_at

    def check_sent_email(self, resume):
        request = self.context.get('request', None)
        if request is None:
            return False
        company = request.user.company
        if not company:
            return False

        contact_profile_exist = resume.contactprofile_set.filter(
            company=company, resume=resume).exists()
        return contact_profile_exist

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
                  "certificates", "languageSkills", "advancedSkills",
                  "lastViewedDate", "isSentEmail")


class SendMailToJobSeekerSerializer(serializers.Serializer):
    fullName = serializers.CharField(max_length=100, required=True)
    title = serializers.CharField(max_length=200, required=True)
    content = serializers.CharField(required=True)

    email = serializers.EmailField(max_length=100, required=True)
    isSendMe = serializers.BooleanField(default=False)

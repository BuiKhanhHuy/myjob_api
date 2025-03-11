import datetime
from datetime import date
import cloudinary.uploader
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


class CompanyImageSerializer(serializers.ModelSerializer):
    imageUrl = serializers.SerializerMethodField(method_name='get_image_url', read_only=True)
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
                raise serializers.ValidationError({'errorMessage': ERROR_MESSAGES["MAXIMUM_IMAGES"]})
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
                company_image = CompanyImage.objects.create(company=request.user.company)
                # Upload the file to Cloudinary
                company_image_upload_result = cloudinary.uploader.upload(
                    file,
                    folder=settings.CLOUDINARY_DIRECTORY["company_image"],
                    public_id=company_image.id
                )
          
                # Create a new File object for the uploaded image
                image = File.objects.create(
                    public_id=company_image_upload_result.get("public_id"),
                    version=company_image_upload_result.get("version"),
                    format=company_image_upload_result.get("format"),
                    resource_type=company_image_upload_result.get("resource_type"),
                    uploaded_at=company_image_upload_result.get("created_at"),
                    bytes=company_image_upload_result.get("bytes"),
                    metadata=company_image_upload_result
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
    employeeSize = serializers.IntegerField(source="employee_size", required=True)
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
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    companyImageUrl = serializers.SerializerMethodField(method_name='get_company_logo_url', read_only=True)
    companyCoverImageUrl = serializers.SerializerMethodField(method_name='get_company_cover_image_url', read_only=True)
    locationDict = common_serializers.LocationSerializer(source="location",
                                                         fields=['city'],
                                                         read_only=True)

    followNumber = serializers.SerializerMethodField(method_name="get_follow_number", read_only=True)
    jobPostNumber = serializers.SerializerMethodField(method_name="get_job_post_number", read_only=True)
    isFollowed = serializers.SerializerMethodField(method_name='check_followed', read_only=True)
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

                # update in firebase
                queue_auth.update_info.delay(instance.user_id, instance.company_name)

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
    companyImageUrl = serializers.SerializerMethodField(method_name='get_company_logo_url', read_only=True)

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
                # Upload the logo to Cloudinary
                logo_upload_result = cloudinary.uploader.upload(file,
                                                                folder=settings.CLOUDINARY_DIRECTORY["logo"],
                                                                public_id=company.id)
                # Prepare the data for the company logo
                company_logo_data = {
                    "public_id": logo_upload_result.get("public_id"),
                    "version": logo_upload_result.get("version"),
                    "format": logo_upload_result.get("format"),
                    "resource_type": logo_upload_result.get("resource_type"),
                    "uploaded_at": logo_upload_result.get("created_at"),
                    "bytes": logo_upload_result.get("bytes"),
                    "metadata": logo_upload_result
                }
                # Check if the company already has a logo
                if company.logo:
                    # Update the existing logo
                    for key, value in company_logo_data.items():
                        setattr(company.logo, key, value)
                    company.logo.save()
                else:
                    # Create a new logo if it doesn't exist
                    company_logo = File.objects.create(**company_logo_data)
                    company.logo = company_logo
                company.save()

                # Update the company avatar in Firebase
                queue_auth.update_avatar.delay(company.user_id, company.logo.get_full_url())

            return company
        except Exception as e:
            # Log the error if any occurs during the process
            helper.print_log_error("update company logo", e)
            return None


class CompanyCoverImageSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True, write_only=True)
    companyCoverImageUrl = serializers.SerializerMethodField(method_name='get_company_cover_image_url', read_only=True)

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
                # Upload the company cover image to Cloudinary
                company_cover_image_upload_result = cloudinary.uploader.upload(file,
                                                                           folder=settings.CLOUDINARY_DIRECTORY[
                                                                               "cover_image"],
                                                                           public_id=company.id)
                # Prepare the data for the company cover image
                company_cover_image_data = {
                    "public_id": company_cover_image_upload_result.get("public_id"),
                    "version": company_cover_image_upload_result.get("version"),
                    "format": company_cover_image_upload_result.get("format"),
                    "resource_type": company_cover_image_upload_result.get("resource_type"),
                    "uploaded_at": company_cover_image_upload_result.get("created_at"),
                    "bytes": company_cover_image_upload_result.get("bytes"),
                    "metadata": company_cover_image_upload_result
                }
                # Check if the company already has a cover image
                if company.cover_image:
                    # Update the existing cover image
                    for key, value in company_cover_image_data.items():
                        setattr(company.cover_image, key, value)
                    company.cover_image.save()
                else:
                    # Create a new cover image if it doesn't exist
                    cover_image_new = File.objects.create(**company_cover_image_data)
                    company.cover_image = cover_image_new
             
            # Save the company instance to reflect the changes
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

        # update in firebase
        queue_auth.update_info.delay(user_obj.id, user_obj.full_name)

        instance.save()
        return instance


class CvSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=200)
    fileUrl = serializers.SerializerMethodField(method_name="get_cv_file_url", read_only=True)
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

        # Upload the PDF file to Cloudinary
        pdf_upload_result = cloudinary.uploader.upload(pdf_file,
                                                       folder=settings.CLOUDINARY_DIRECTORY["cv"],
                                                       public_id=instance.id)
        
        # Prepare the data for the PDF file
        pdf_data = {
            "public_id": pdf_upload_result.get("public_id"),
            "version": pdf_upload_result.get("version"),
            "format": pdf_upload_result.get("format"),
            "resource_type": pdf_upload_result.get("resource_type"),
            "uploaded_at": pdf_upload_result.get("created_at"),
            "bytes": pdf_upload_result.get("bytes"),
            "metadata": pdf_upload_result
        }
        
        # Update or create the PDF file
        if instance.file:
            # Update existing PDF file
            for key, value in pdf_data.items():
                setattr(instance.file, key, value)
            instance.file.save()
        else:
            # Create a new PDF file if it doesn't exist
            instance.file = File.objects.create(**pdf_data)
        
        # Save the instance to ensure any other changes are persisted
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
    imageUrl = serializers.SerializerMethodField(method_name="get_cv_image_url", read_only=True)
    fileUrl = serializers.SerializerMethodField(method_name="get_cv_file_url", read_only=True)
    file = serializers.FileField(required=True, write_only=True)
    user = auth_serializers.UserSerializer(fields=["id", "fullName", "avatarUrl"], read_only=True)

    isSaved = serializers.SerializerMethodField(method_name='check_saved', read_only=True)
    viewEmployerNumber = serializers.SerializerMethodField(method_name="get_view_number", read_only=True)
    userDict = auth_serializers.UserSerializer(source='user', fields=["id", "fullName"], read_only=True)
    jobSeekerProfileDict = JobSeekerProfileSerializer(source="job_seeker_profile",
                                                      fields=["id", "old"],
                                                      read_only=True)
    lastViewedDate = serializers.SerializerMethodField(method_name='get_last_viewed_date', read_only=True)
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
        resume_viewed = ResumeViewed.objects.filter(company=company, resume=resume).first()
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
                  "type")

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
            pdf_upload_result = cloudinary.uploader.upload(pdf_file,
                                                           folder=settings.CLOUDINARY_DIRECTORY["cv"],
                                                           public_id=resume.id)

            # Create a new File instance with the details from the Cloudinary upload result
            cv_file = File.objects.create(
                public_id=pdf_upload_result.get('public_id'),
                version=pdf_upload_result.get('version'),
                format=pdf_upload_result.get('format'),
                resource_type=pdf_upload_result.get('resource_type'),
                uploaded_at=pdf_upload_result.get('created_at'),
                bytes=pdf_upload_result.get('bytes'),
                metadata=pdf_upload_result
            )

            # Associate the uploaded file with the resume and save the changes
            resume.file = cv_file
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
    trainingPlaceName = serializers.CharField(source='training_place_name', read_only=True)
    startDate = serializers.DateField(source='start_date', read_only=True)
    completedDate = serializers.DateField(source='completed_date', read_only=True)
    description = serializers.CharField(read_only=True)

    class Meta:
        model = EducationDetail
        fields = ('id', 'degreeName', 'major', 'trainingPlaceName',
                  'startDate', 'completedDate', 'description')


class CertificatePdfSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    trainingPlace = serializers.CharField(source='training_place', read_only=True)
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
    academicLevel = serializers.IntegerField(source="academic_level", read_only=True, )
    typeOfWorkplace = serializers.IntegerField(source="type_of_workplace", read_only=True, )
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
    experienceDetails = ExperiencePdfSerializer(source='experience_details', read_only=True, many=True)
    educationDetails = EducationPdfSerializer(source='education_details', read_only=True, many=True)
    certificates = CertificatePdfSerializer(read_only=True, many=True)
    languageSkills = LanguageSkillPdfSerializer(source='language_skills', read_only=True, many=True)
    advancedSkills = AdvancedSkillPdfSerializer(source='advanced_skills', read_only=True, many=True)

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
    title = serializers.PrimaryKeyRelatedField(source="resume.title", read_only=True)
    fullName = serializers.PrimaryKeyRelatedField(source="resume.user.full_name", read_only=True)
    email = serializers.PrimaryKeyRelatedField(source="resume.user.email", read_only=True)
    phone = serializers.PrimaryKeyRelatedField(source="resume.job_seeker_profile.phone", read_only=True)
    gender = serializers.PrimaryKeyRelatedField(source="resume.job_seeker_profile.gender", read_only=True)

    birthday = serializers.PrimaryKeyRelatedField(source="resume.job_seeker_profile.birthday", read_only=True)
    address = serializers.PrimaryKeyRelatedField(source="resume.job_seeker_profile.location.city.name", read_only=True)
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

    # slug field for web
    resume = serializers.SlugRelatedField(required=False, slug_field="slug", queryset=Resume.objects.all())
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
            raise serializers.ValidationError({'errorMessage': ERROR_MESSAGES["MAXIMUM_EDUCATION"]})
        return attrs

    class Meta:
        model = EducationDetail
        fields = ('id', 'degreeName', 'major', 'trainingPlaceName',
                  'startDate', 'completedDate', 'description', 'resume', 'resumeId')


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

    # slug field for web
    resume = serializers.SlugRelatedField(required=False, slug_field="slug", queryset=Resume.objects.all())
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
            raise serializers.ValidationError({'errorMessage': ERROR_MESSAGES["MAXIMUM_EXPERIENCE"]})
        return attrs

    class Meta:
        model = ExperienceDetail
        fields = ('id', 'jobName', 'companyName',
                  'startDate', 'endDate',
                  'description', 'resume', 'resumeId')


class CertificateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200)
    trainingPlace = serializers.CharField(source='training_place', required=True, max_length=255)
    startDate = serializers.DateField(source='start_date', required=True,
                                      input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                     var_sys.DATE_TIME_FORMAT["Ymd"]])
    expirationDate = serializers.DateField(source='expiration_date', required=False, allow_null=True,
                                           input_formats=[var_sys.DATE_TIME_FORMAT["ISO8601"],
                                                          var_sys.DATE_TIME_FORMAT["Ymd"]])

    # slug field for web
    resume = serializers.SlugRelatedField(required=False, slug_field="slug", queryset=Resume.objects.all())
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
            raise serializers.ValidationError({'errorMessage': ERROR_MESSAGES["MAXIMUM_CERTIFICATE"]})
        return attrs

    class Meta:
        model = Certificate
        fields = ('id', 'name', 'trainingPlace', 'startDate',
                  'expirationDate', 'resume', 'resumeId')


class LanguageSkillSerializer(serializers.ModelSerializer):
    language = serializers.IntegerField(required=True)
    level = serializers.IntegerField(required=True)

    # slug field for web
    resume = serializers.SlugRelatedField(required=False, slug_field="slug", queryset=Resume.objects.all())
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
    resume = serializers.SlugRelatedField(required=False, slug_field="slug", queryset=Resume.objects.all())
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
            raise serializers.ValidationError({'errorMessage': ERROR_MESSAGES["MAXIMUM_ADVANCED"]})
        return attrs

    class Meta:
        model = AdvancedSkill
        fields = ('id', 'name', 'level', 'resume', "resumeId")


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
    lastViewedDate = serializers.SerializerMethodField(method_name='get_last_viewed_date', read_only=True)
    isSentEmail = serializers.SerializerMethodField(method_name='check_sent_email', read_only=True)

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
        resume_viewed = ResumeViewed.objects.filter(company=company, resume=resume).first()
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

        contact_profile_exist = resume.contactprofile_set.filter(company=company, resume=resume).exists()
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

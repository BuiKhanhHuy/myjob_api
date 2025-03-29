import concurrent.futures
import cloudinary.uploader
from django.conf import settings
from django.contrib import admin
from django import forms
from django.utils.html import mark_safe
from django.db import transaction
from helpers import helper
from myjob_api.admin import custom_admin_site
from configs import variable_system as var_sys
from common.models import File
from .models import (
    JobSeekerProfile,
    Resume,
    EducationDetail,
    ExperienceDetail,
    Certificate,
    LanguageSkill,
    AdvancedSkill,
    CompanyFollowed,
    Company,
    CompanyImage,
    ResumeSaved,
    ResumeViewed,

)
from django_admin_listfilter_dropdown.filters import (DropdownFilter, ChoiceDropdownFilter)


class CompanyImageInlineForm(forms.ModelForm):
    image_file = forms.FileField(required=False)

    class Meta:
        model = CompanyImage
        fields = '__all__'


class CompanyForm(forms.ModelForm):
    company_image_file = forms.FileField(required=False)
    company_cover_image_file = forms.FileField(required=False)

    class Meta:
        model = Company
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_image_file'].required = False
        self.fields['company_cover_image_file'].required = False


class ResumeForm(forms.ModelForm):
    resume_file = forms.FileField(required=False)

    class Meta:
        model = Company
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resume_file'].required = False


class ResumeViewedForm(forms.ModelForm):
    class Meta:
        model = ResumeViewed
        fields = '__all__'


# INLINE
class EducationDetailInlineAdmin(admin.StackedInline):
    model = EducationDetail
    fk_name = 'resume'
    extra = 1


class ExperienceDetailInlineAdmin(admin.StackedInline):
    model = ExperienceDetail
    fk_name = 'resume'
    extra = 1


class CertificateInlineAdmin(admin.StackedInline):
    model = Certificate
    fk_name = 'resume'
    extra = 1


class LanguageSkillInlineAdmin(admin.StackedInline):
    model = LanguageSkill
    fk_name = 'resume'
    extra = 1


class AdvancedSkillInlineAdmin(admin.StackedInline):
    model = AdvancedSkill
    fk_name = 'resume'
    extra = 1


class CompanyImageInlineAdmin(admin.StackedInline):
    model = CompanyImage
    fk_name = 'company'
    extra = 1
    max_num = 5
    fields = ('show_image',)
    readonly_fields = ('show_image',)
    form = CompanyImageInlineForm

    def show_image(self, company_image):
        # Initialize default values for image URL and alt text
        image_url = var_sys.NO_IMAGE
        image_alt = "No image"
        
        # Retrieve the company image
        image = company_image.image
        # If an image exists, update the URL and alt text
        if image:
            image_url = image.get_full_url()  # Get the full URL of the image
            image_alt = company_image.company.company_name  # Use the company name as alt text
            
        # Return HTML code for displaying the company image
        return mark_safe(
            r"""<img src='{0}'
            alt='{1}' style="border-radius: 2px;object-fit:cover;" width='45px' height='45px'/>""".format(
                image_url, image_alt)
        )


# ADMIN
class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "phone", "birthday", "gender", "marital_status", "location")
    list_display_links = ("id", "user",)
    search_fields = ("id", "user__email", "phone")
    readonly_fields = ('user',)
    list_filter = [
        ("gender", ChoiceDropdownFilter),
        ("marital_status", ChoiceDropdownFilter),
    ]
    list_per_page = 25

    raw_id_fields = ('location',)
    list_select_related = ('user', 'location')


class ResumeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "position", "experience", "academic_level",
                    "type_of_workplace", "job_type", "is_active",)
    list_display_links = ("id", "user", "title",)
    search_fields = ("id", "title", "user__email")
    list_filter = [
        ("position", ChoiceDropdownFilter),
        ("experience", ChoiceDropdownFilter),
        ("academic_level", ChoiceDropdownFilter),
        ("type_of_workplace", ChoiceDropdownFilter),
        ("job_type", ChoiceDropdownFilter),
        ("is_active", DropdownFilter),
    ]
    ordering = ('is_active',)
    readonly_fields = ("type", 'show_resume_image',
                       'job_seeker_profile', 'user')
    inlines = (EducationDetailInlineAdmin, ExperienceDetailInlineAdmin,
               CertificateInlineAdmin, LanguageSkillInlineAdmin,
               AdvancedSkillInlineAdmin)
    list_per_page = 25
    fields = ("title", "salary_min", "salary_max",
              "position", "experience", "academic_level",
              "type_of_workplace", "job_type", "city", "career",
              "job_seeker_profile", "user", "type",
              "is_active", "show_resume_image", "resume_file",
              "description")

    autocomplete_fields = ['city', 'career',
                           'company_viewers', 'company_savers']
    list_select_related = ('city', 'career',)

    def show_resume_image(self, resume):
        # Check if there is a resume
        if resume:
            # Get the cv file of the resume
            cv_file = resume.file
            # Set the default alt for the image to "No image"
            image_alt = "No image"
            # Set the default URL for the image to the default avatar URL
            image_url = var_sys.AVATAR_DEFAULT["AVATAR"]
            # If there is an image, change the URL and alt of the image
            if cv_file:
                # Prepare data for image file derived from PDF
                image_url = cv_file.get_full_url().replace(f".{cv_file.format}", ".jpg")
                image_alt = resume.title
            # Return the image that has been formatted for safe display
            return mark_safe(
                f"<img src='{image_url}' alt='{image_alt}' style='border-radius: 2px;object-fit:cover;' width='45px' height='45px'/>"
            )

    show_resume_image.short_description = "Resume image"

    form = ResumeForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        resume_file = request.FILES.get('resume_file', None)
        if resume_file:
            try:
                with transaction.atomic():
                    public_id = None
                    # Overwrite if image already exists
                    if obj.file:
                        path_list = obj.file.public_id.split('/')
                        public_id = path_list[-1] if path_list else None
                    # Upload PDF to cloudinary
                    pdf_upload_result = cloudinary.uploader.upload(
                        resume_file,
                        folder=settings.CLOUDINARY_DIRECTORY["cv"],
                        public_id=public_id
                    )
                    
                    # Prepare data for PDF file
                    pdf_data = {
                        "public_id": pdf_upload_result.get("public_id"),
                        "version": pdf_upload_result.get("version"),
                        "format": pdf_upload_result.get("format"),
                        "resource_type": pdf_upload_result.get("resource_type"),
                        "uploaded_at": pdf_upload_result.get("created_at"),
                        "bytes": pdf_upload_result.get("bytes"),
                        "metadata": pdf_upload_result
                    }
                    
                    # Update or create PDF file
                    if obj.file:
                        for key, value in pdf_data.items():
                            setattr(obj.file, key, value)
                        obj.file.save()
                    else:
                        pdf_file = File.objects.create(**pdf_data)
                        obj.file = pdf_file

                    obj.save()

            except Exception as ex:
                helper.print_log_error("resume_save_model", ex)


class CompanyAdmin(admin.ModelAdmin):
    inlines = [CompanyImageInlineAdmin]
    list_display = ("id", "company_name", "field_operation", "company_email",
                    "company_phone", "employee_size", "tax_code", "user",)
    list_display_links = ("id", "company_name",)
    search_fields = ("id", "company_name", "field_operation", "company_email", "company_phone", "tax_code")
    list_filter = [
        ("employee_size", ChoiceDropdownFilter),
    ]
    readonly_fields = ('show_company_image', 'show_company_cover_image')
    list_per_page = 25

    raw_id_fields = ('user', 'location', 'followers')
    list_select_related = ('user', 'location')

    fieldsets = (
        (None, {
            'fields': ("company_name", 'field_operation', 'company_phone',
                       'employee_size', 'tax_code', 'since', 'description',
                       'website_url', 'user', 'location')
        }),
        ('Media', {
            'fields': ('show_company_image', 'company_image_file',
                       'show_company_cover_image', 'company_cover_image_file')
        }),
        ('Social network', {
            'fields': ('facebook_url', 'youtube_url', 'linkedin_url')
        }),
    )

    def show_company_image(self, company):
        # Set default values for company logo URL and alt text
        company_logo_url = var_sys.NO_IMAGE
        company_logo_alt = "No image"
        
        # Get company logo and update URL and alt text if logo exists
        company_logo = company.logo
        if company_logo:
            company_logo_url = company_logo.get_full_url()
            company_logo_alt = company.company_name
           
        # Return HTML code for displaying the company logo
        return mark_safe(
            r"""<img src='{0}'
            alt='{1}' style="border-radius: 2px;object-fit:cover;" width='45px' height='45px'/>""".format(
                company_logo_url, company_logo_alt)
        )

    show_company_image.short_description = "Logo"

    def show_company_cover_image(self, company):
        # Initialize default values for company cover image URL and alt text
        company_cover_image_url = var_sys.NO_IMAGE
        company_cover_image_alt = "No image"
        
        # Retrieve the company cover image
        company_cover_image = company.cover_image
        # If a cover image exists, update the URL and alt text
        if company_cover_image:
            company_cover_image_url = company_cover_image.get_full_url()
            company_cover_image_alt = company.company_name
            
        # Return HTML code for displaying the company cover image
        return mark_safe(
            r"""<img src='{0}'
            alt='{1}' style="border-radius: 2px;object-fit:cover;" width='45px' height='45px'/>""".format(
                company_cover_image_url, company_cover_image_alt)
        )

    show_company_cover_image.short_description = "Cover image"

    form = CompanyForm

    def save_model(self, request, company, form, change):
        super().save_model(request, company, form, change)
        files = request.FILES

        # logo and cover_image
        logo_file = files.pop('company_image_file', None)
        company_cover_image_file = files.pop('company_cover_image_file', None)

        # media
        company_image_files = files
        for a in company_image_files:
            print(a)

        # Update company logo
        if logo_file:
            try:
                with transaction.atomic():
                    public_id = None
                    # Overwrite if image already exists
                    if company.logo:
                        path_list = company.logo.public_id.split('/')
                        public_id = path_list[-1] if path_list else None
                    # Upload logo to cloudinary
                    logo_upload_result = cloudinary.uploader.upload(
                        logo_file,
                        folder=settings.CLOUDINARY_DIRECTORY["logo"],
                        public_id=public_id
                    )
                    
                    # Prepare data for logo
                    company_logo_data = {
                        "public_id": logo_upload_result.get("public_id"),
                        "version": logo_upload_result.get("version"),
                        "format": logo_upload_result.get("format"),
                        "resource_type": logo_upload_result.get("resource_type"),
                        "uploaded_at": logo_upload_result.get("created_at"),
                        "bytes": logo_upload_result.get("bytes"),
                        "metadata": logo_upload_result
                    }
                    
                    # Update or create logo
                    if company.logo:
                        for key, value in company_logo_data.items():
                            setattr(company.logo, key, value)
                        company.logo.save()
                    else:
                        company_logo_new = File.objects.create(**company_logo_data)
                        company.logo = company_logo_new
            except Exception as ex:
                helper.print_log_error("company_image_save_model", ex)

        # Update company cover image
        if company_cover_image_file:
            try:
                with transaction.atomic():
                    public_id = None
                    # Overwrite if image already exists
                    if company.cover_image:
                        path_list = company.cover_image.public_id.split('/')
                        public_id = path_list[-1] if path_list else None
                    # Upload cover image to cloudinary
                    company_cover_image_upload_result = cloudinary.uploader.upload(
                        company_cover_image_file,
                        folder=settings.CLOUDINARY_DIRECTORY["cover_image"],
                        public_id=public_id
                    )

                    # Prepare data for cover image
                    company_cover_image_data = {
                        "public_id": company_cover_image_upload_result.get("public_id"),
                        "version": company_cover_image_upload_result.get("version"),
                        "format": company_cover_image_upload_result.get("format"),
                        "resource_type": company_cover_image_upload_result.get("resource_type"),
                        "uploaded_at": company_cover_image_upload_result.get("created_at"),
                        "bytes": company_cover_image_upload_result.get("bytes"),
                        "metadata": company_cover_image_upload_result
                    }
                    
                    # Update or create cover image
                    if company.cover_image:
                        for key, value in company_cover_image_data.items():
                            setattr(company.cover_image, key, value)
                        company.cover_image.save()
                    else:
                        company_cover_image_new = File.objects.create(**company_cover_image_data)
                        company.cover_image = company_cover_image_new
            except Exception as ex:
                helper.print_log_error("company_cover_image_save_model", ex)

        if logo_file or company_cover_image_file:
            # Save company
            company.save()

        # save company image
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self._upload_file, company_image_files)

    def _upload_file(self, file):
        # TODO:
        print("UPLOAD: ", file)


class ResumeSavedAdmin(admin.ModelAdmin):
    list_display = ("id", "resume", "company")
    list_display_links = ("id",)
    search_fields = ("id", "resume__title", "company__company_email", "company__company_name")
    list_per_page = 25

    readonly_fields = ('resume', 'company')
    list_select_related = ('resume', 'company')


class ResumeViewedAdmin(admin.ModelAdmin):
    list_display = ("id", "resume", "company", "views")
    list_display_links = ("id",)
    ordering = ('views', 'id')
    search_fields = ("id", "resume__title", "company__company_email", "company__company_name")
    list_per_page = 25

    readonly_fields = ('resume', 'company')
    list_select_related = ('resume', 'company')

    form = ResumeViewedForm


class CompanyFollowedAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "user")
    list_display_links = ("id",)
    search_fields = ("id", "company__company_name", "user__email")
    list_per_page = 25

    raw_id_fields = ('company', 'user')
    list_select_related = ('company', 'user')


custom_admin_site.register(JobSeekerProfile, JobSeekerProfileAdmin)
custom_admin_site.register(Resume, ResumeAdmin)
custom_admin_site.register(Company, CompanyAdmin)
custom_admin_site.register(ResumeSaved, ResumeSavedAdmin)
custom_admin_site.register(ResumeViewed, ResumeViewedAdmin)
custom_admin_site.register(CompanyFollowed, CompanyFollowedAdmin)

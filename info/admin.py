"""
MyJob Recruitment System - Part of MyJob Platform

Author: Bui Khanh Huy
Email: khuy220@gmail.com
Copyright (c) 2023 Bui Khanh Huy

License: MIT License
See the LICENSE file in the project root for full license information.
"""

import concurrent.futures
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
from helpers.cloudinary_service import CloudinaryService


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
                alt='{1}' style="border-radius: 2px;object-fit:cover;" width='450px' height='175px'/>""".format(
                    image_url, image_alt)
            )
        return mark_safe(
            r"""<img src='{0}'
            alt='{1}' style="border-radius: 2px;object-fit:cover;" width='45px' height='45px'/>""".format(
                image_url, image_alt)
        )

    show_image.short_description = "Image"

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
                    "type_of_workplace", "job_type", "type", "is_active",)
    list_display_links = ("id", "user", "title",)
    search_fields = ("id", "title", "user__email")
    list_filter = [
        ("position", ChoiceDropdownFilter),
        ("experience", ChoiceDropdownFilter),
        ("academic_level", ChoiceDropdownFilter),
        ("type_of_workplace", ChoiceDropdownFilter),
        ("job_type", ChoiceDropdownFilter),
        ("type", DropdownFilter),
        ("is_active", DropdownFilter),
    ]
    ordering = ('is_active',)
    readonly_fields = ("type", 'preview_pdf',
                       'job_seeker_profile', 'user')
    inlines = (EducationDetailInlineAdmin, ExperienceDetailInlineAdmin,
               CertificateInlineAdmin, LanguageSkillInlineAdmin,
               AdvancedSkillInlineAdmin)
    list_per_page = 25
    fields = ("title", "salary_min", "salary_max",
              "position", "experience", "academic_level",
              "type_of_workplace", "job_type", "city", "career",
              "job_seeker_profile", "user", "type", 'preview_pdf', "resume_file",
              "description", "is_active")

    autocomplete_fields = ['city', 'career',
                           'company_viewers', 'company_savers']
    list_select_related = ('city', 'career',)

    def preview_pdf(self, resume):
        if resume.file:
            cv_file = resume.file
            return mark_safe(f'<iframe src="{cv_file.get_full_url()}" width="1000" height="800"></iframe>')
        return "---"

    preview_pdf.short_description = "CV Preview"

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
                    pdf_upload_result = CloudinaryService.upload_image(
                        resume_file,
                        settings.CLOUDINARY_DIRECTORY["cv"],
                        public_id=public_id
                    )
                    # Update or create file
                    obj.file = File.update_or_create_file_with_cloudinary(
                        obj.file,
                        pdf_upload_result,
                        File.CV_TYPE
                    )
                    obj.save()

            except Exception as ex:
                helper.print_log_error("resume_save_model", ex)


class CompanyAdmin(admin.ModelAdmin):
    inlines = [CompanyImageInlineAdmin]
    list_display = ("id", "show_company_image", "company_name", "field_operation", "company_email",
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
            alt='{1}' style="border-radius: 2px;object-fit:contain;" width='45px' height='45px'/>""".format(
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
            alt='{1}' style="border-radius: 2px;object-fit:cover;" width='450px' height='175px'/>""".format(
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
                    logo_upload_result = CloudinaryService.upload_image(
                        logo_file,
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
                    company_cover_image_upload_result = CloudinaryService.upload_image(
                        company_cover_image_file,
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

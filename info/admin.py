import concurrent.futures
import cloudinary.uploader
from django.conf import settings
from django.contrib import admin
from django import forms
from django.utils.html import mark_safe
from helpers import helper
from myjob_api.admin import custom_admin_site
from configs import variable_system as var_sys
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
    fields = ('show_image', 'image_file', 'image_public_id', 'image_url')
    readonly_fields = ('show_image', 'image_public_id', 'image_url')
    form = CompanyImageInlineForm

    def show_image(self, company_image):
        if company_image:
            if company_image.image_url:
                return mark_safe(
                    r"""<img src='{0}'
                    alt='{1}' style="border-radius: 50px;object-fit:cover;" width='50px' height='50px'/>""".format(
                        company_image.image_url,
                        company_image.company.company_name)
                )
            else:
                return mark_safe(
                    r"""<img src='{0}'
                    alt='{1}' style="border-radius: 2px;object-fit:cover;" width='45px' height='45px'/>""".format(
                        var_sys.NO_IMAGE, "No image")
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
    readonly_fields = ("type", 'public_id', 'show_resume_image',
                       'job_seeker_profile', 'user')
    inlines = (EducationDetailInlineAdmin, ExperienceDetailInlineAdmin,
               CertificateInlineAdmin, LanguageSkillInlineAdmin,
               AdvancedSkillInlineAdmin)
    list_per_page = 25
    fields = ("title", "salary_min", "salary_max",
              "position", "experience", "academic_level",
              "type_of_workplace", "job_type", "city", "career",
              "job_seeker_profile", "user", "public_id", "type",
              "is_active", "show_resume_image", "resume_file",
              "description")

    autocomplete_fields = ['city', 'career',
                           'company_viewers', 'company_savers']
    list_select_related = ('city', 'career',)

    def show_resume_image(self, resume):
        if resume:
            if resume.image_url:
                return mark_safe(
                    r"""<img src='{0}'
                    alt='{1}' style="border-radius: 20px;object-fit:cover;" width='' height='200px'/>""".format(
                        resume.image_url,
                        resume.title)
                )
            else:
                return mark_safe(
                    r"""<img src='{0}'
                    alt='{1}' style="border-radius: 2px;object-fit:cover;" width='45px' height='45px'/>""".format(
                        var_sys.NO_IMAGE, "No image")
                )

    show_resume_image.short_description = "Resume image"

    form = ResumeForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        resume_file = request.FILES.get('resume_file', None)
        if resume_file:
            try:
                pdf_upload_result = cloudinary.uploader.upload(resume_file,
                                                               folder=settings.CLOUDINARY_DIRECTORY["cv"],
                                                               public_id=obj.id)
                pdf_upload_url = pdf_upload_result["secure_url"]
                pdf_public_id = pdf_upload_result.get('public_id')
                image_url = cloudinary.utils.cloudinary_url(pdf_public_id + ".jpg")[0]

            except Exception as ex:
                helper.print_log_error("resume_save_model", ex)
            else:
                obj.file_url = pdf_upload_url
                obj.public_id = pdf_public_id
                obj.image_url = image_url
                obj.save()


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
        if company:
            if company.company_image_url:
                return mark_safe(
                    r"""<img src='{0}'
                    alt='{1}' style="border-radius: 50px;object-fit:cover;" width='50px' height='50px'/>""".format(
                        company.company_image_url,
                        company.company_name)
                )
            else:
                return mark_safe(
                    r"""<img src='{0}'
                    alt='{1}' style="border-radius: 2px;object-fit:cover;" width='45px' height='45px'/>""".format(
                        var_sys.NO_IMAGE, "No image")
                )

    show_company_image.short_description = "Logo"

    def show_company_cover_image(self, company):
        if company:
            if company.company_cover_image_url:
                return mark_safe(
                    r"""<img src='{0}'
                    alt='{1}' style="border-radius: 5px;" width='75%' height='220px'/>""".format(
                        company.company_cover_image_url,
                        company.company_name)
                )
            else:
                return mark_safe(
                    r"""<img src='{0}'
                    alt='{1}' style="border-radius: 2px;object-fit:cover;" width='45px' height='45px'/>""".format(
                        var_sys.NO_IMAGE, "No image")
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

        # save company
        if logo_file:
            try:
                company_image_upload_result = cloudinary.uploader.upload(
                    logo_file,
                    folder=settings.CLOUDINARY_DIRECTORY[
                        "logo"],
                    public_id=company.id
                )
                company_image_url = company_image_upload_result.get('secure_url')
                company_image_public_id = company_image_upload_result.get('public_id')
            except Exception as ex:
                helper.print_log_error("company_image_save_model", ex)
            else:
                company.company_image_url = company_image_url
                company.company_image_public_id = company_image_public_id

        if company_cover_image_file:
            try:
                company_cover_image_upload_result = cloudinary.uploader.upload(
                    company_cover_image_file,
                    folder=settings.CLOUDINARY_DIRECTORY[
                        "coverImage"],
                    public_id=company.id
                )
                company_cover_image_url = company_cover_image_upload_result.get('secure_url')
                company_cover_image_public_id = company_cover_image_upload_result.get('public_id')
            except Exception as ex:
                helper.print_log_error("company_cover_image_save_model", ex)
            else:
                company.company_cover_image_url = company_cover_image_url
                company.company_cover_image_public_id = company_cover_image_public_id

        if logo_file or company_cover_image_file:
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

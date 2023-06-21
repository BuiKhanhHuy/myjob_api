import cloudinary.uploader
from django.conf import settings
from django.contrib import admin
from django import forms
from django.utils.html import mark_safe
from helpers import helper
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
from django_admin_listfilter_dropdown.filters import (DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter)


class CompanyForm(forms.ModelForm):
    company_image_file = forms.FileField(required=False)
    company_cover_image_file = forms.FileField(required=False)

    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'website_url': forms.URLInput(attrs={'class': "form-control"}),
            'facebook_url': forms.URLInput(attrs={'class': "form-control"}),
            'youtube_url': forms.URLInput(attrs={'class': "form-control"}),
            'linkedin_url': forms.URLInput(attrs={'class': "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_image_file'].required = False
        self.fields['company_cover_image_file'].required = False


class ResumeForm(forms.ModelForm):
    resume_file = forms.FileField(required=False)

    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'salary_min': forms.NumberInput(attrs={'class': "form-control"}),
            'salary_max': forms.NumberInput(attrs={'class': "form-control"}),
            'is_active': forms.CheckboxInput(attrs={'class': "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resume_file'].required = False


class ResumeViewedForm(forms.ModelForm):
    class Meta:
        model = ResumeViewed
        fields = '__all__'
        widgets = {
            'views': forms.NumberInput(attrs={'class': "form-control"}),
        }


# INLINE
class EducationDetailInlineAdmin(admin.StackedInline):
    model = EducationDetail
    classes = ('collapse',)
    fk_name = 'resume'
    extra = 1


class ExperienceDetailInlineAdmin(admin.StackedInline):
    model = ExperienceDetail
    classes = ('collapse',)
    fk_name = 'resume'
    extra = 1


class CertificateInlineAdmin(admin.StackedInline):
    model = Certificate
    classes = ('collapse',)
    fk_name = 'resume'
    extra = 1


class LanguageSkillInlineAdmin(admin.StackedInline):
    model = LanguageSkill
    classes = ('collapse',)
    fk_name = 'resume'
    extra = 1


class AdvancedSkillInlineAdmin(admin.StackedInline):
    model = AdvancedSkill
    classes = ('collapse',)
    fk_name = 'resume'
    extra = 1


class CompanyImageInlineAdmin(admin.StackedInline):
    model = CompanyImage
    classes = ('collapse',)
    fk_name = 'company'
    extra = 1


# ADMIN
@admin.register(JobSeekerProfile)
class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "birthday", "gender", "marital_status", "location")
    list_display_links = ("user",)
    search_fields = ("user__email", "phone")
    readonly_fields = ('user',)
    list_filter = [
        ("gender", ChoiceDropdownFilter),
        ("marital_status", ChoiceDropdownFilter),
    ]
    list_per_page = 25

    raw_id_fields = ('location',)
    list_select_related = ('user', 'location')


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("title", "position", "experience", "academic_level",
                    "type_of_workplace", "job_type", "is_active", "user")
    list_display_links = ("title",)
    search_fields = ("title", "user__email")
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
            return mark_safe(
                r"""<img src='{0}'
                alt='{1}' style="border-radius: 20px;object-fit:cover;" width='200px' height='200px'/>""".format(
                    resume.image_url if resume.image_url else "https://diskominfo.mataramkota.go.id/themes/kenshin-kenshinschool/assets/images/default.jpg",
                    resume.title)
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


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "company_name", "field_operation", "company_email",
                    "company_phone", "employee_size", "tax_code", "user",)
    list_display_links = ("id", "company_name",)
    search_fields = ("company_name", "field_operation", "company_email", "company_phone", "tax_code")
    list_filter = [
        ("employee_size", ChoiceDropdownFilter),
    ]
    readonly_fields = ('show_company_image', 'show_company_cover_image')
    inlines = (CompanyImageInlineAdmin,)
    list_per_page = 25

    raw_id_fields = ('user', 'location', 'followers')
    list_select_related = ('user', 'location')

    fields = (
        "company_name",
        "field_operation",
        "company_email",
        "company_phone",
        "employee_size",
        "tax_code",
        "since",
        "website_url",
        "facebook_url",
        "youtube_url",
        "linkedin_url",
        "user",
        "location",
        'show_company_image',
        "company_image_file",
        'show_company_cover_image',
        "company_cover_image_file",
        "description",
    )

    def show_company_image(self, company):
        if company:
            return mark_safe(
                r"""<img src='{0}'
                alt='{1}' style="border-radius: 50px;object-fit:cover;" width='50px' height='50px'/>""".format(
                    company.company_image_url,
                    company.company_name)
            )

    show_company_image.short_description = "Logo"

    def show_company_cover_image(self, company):
        if company:
            return mark_safe(
                r"""<img src='{0}'
                alt='{1}' style="border-radius: 5px;" width='75%' height='200px'/>""".format(
                    company.company_cover_image_url,
                    company.company_name)
            )

    show_company_cover_image.short_description = "Cover image"

    form = CompanyForm

    def save_model(self, request, company, form, change):
        super().save_model(request, company, form, change)

        logo_file = request.FILES.get('company_image_file', None)
        company_cover_image_file = request.FILES.get('company_cover_image_file', None)

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


@admin.register(ResumeSaved)
class ResumeSavedAdmin(admin.ModelAdmin):
    list_display = ("id", "resume", "company")
    list_display_links = ("id",)
    search_fields = ("resume__title", "company__company_email", "company__company_name")
    list_per_page = 25

    readonly_fields = ('resume', 'company')
    list_select_related = ('resume', 'company')


@admin.register(ResumeViewed)
class ResumeViewedAdmin(admin.ModelAdmin):
    list_display = ("id", "resume", "company", "views")
    list_display_links = ("id",)
    ordering = ('views', 'id')
    search_fields = ("resume__title", "company__company_email", "company__company_name")
    list_per_page = 25

    readonly_fields = ('resume', 'company')
    list_select_related = ('resume', 'company')

    form = ResumeViewedForm


@admin.register(CompanyFollowed)
class CompanyFollowedAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "user")
    list_display_links = ("id",)
    search_fields = ("company__company_name", "user__email")
    list_per_page = 25

    raw_id_fields = ('company', 'user')
    list_select_related = ('company', 'user')

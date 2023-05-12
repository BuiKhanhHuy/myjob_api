from django.contrib import admin
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
class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "birthday", "gender", "marital_status", "location")
    list_display_links = ("user",)
    search_fields = ("user__email", "phone")
    list_filter = [
        ("gender", ChoiceDropdownFilter),
        ("marital_status", ChoiceDropdownFilter),
    ]
    # readonly_fields = ("show_avatar", "avatar_public_id", "avatar_url", "password")
    list_per_page = 25


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
    readonly_fields = ("image_url", "file_url", "public_id", "type")
    inlines = (EducationDetailInlineAdmin, ExperienceDetailInlineAdmin,
               CertificateInlineAdmin, LanguageSkillInlineAdmin,
               AdvancedSkillInlineAdmin)
    list_per_page = 25


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("company_name", "field_operation", "company_email",
                    "company_phone", "employee_size", "tax_code", "user",)
    list_display_links = ("company_name",)
    search_fields = ("company_name", "field_operation", "company_email", "company_phone", "tax_code")
    list_filter = [
        ("employee_size", ChoiceDropdownFilter),
    ]
    readonly_fields = ("company_image_url", "company_image_public_id",
                       "company_cover_image_url", "company_cover_image_public_id")
    inlines = (CompanyImageInlineAdmin,)
    list_per_page = 25


class ResumeSavedAdmin(admin.ModelAdmin):
    list_display = ("id", "resume", "company")
    list_display_links = ("id",)
    search_fields = ("resume__title", "company__company_email", "company__company_name")
    list_per_page = 25


class ResumeViewedAdmin(admin.ModelAdmin):
    list_display = ("id", "resume", "company", "views")
    list_display_links = ("id",)
    ordering = ('views', 'id')
    search_fields = ("resume__title", "company__company_email", "company__company_name")
    list_per_page = 25


class CompanyFollowedAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "user")
    list_display_links = ("id",)
    search_fields = ("company__company_name", "user__email")
    list_filter = [
        ("company", RelatedDropdownFilter),
        ("user", RelatedDropdownFilter),
    ]
    list_per_page = 25


admin.site.register(JobSeekerProfile, JobSeekerProfileAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(ResumeSaved, ResumeSavedAdmin)
admin.site.register(ResumeViewed, ResumeViewedAdmin)
admin.site.register(CompanyFollowed, CompanyFollowedAdmin)

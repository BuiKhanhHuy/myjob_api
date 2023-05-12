from django.contrib import admin
from .models import (
    JobPost,
    SavedJobPost,
    JobPostActivity
)
from django_admin_listfilter_dropdown.filters import (RelatedDropdownFilter, DropdownFilter, ChoiceDropdownFilter)


class JobPostAdmin(admin.ModelAdmin):
    list_display = ("id", "job_name", "career", "deadline", "quantity", "is_hot",
                    "is_urgent", "is_verify", "views", "shares")
    list_display_links = ("id", "job_name",)
    list_editable = ("is_hot", "is_urgent", "is_verify")
    search_fields = ("job_name", "career__name")
    list_filter = [
        ("is_hot", DropdownFilter),
        ("is_urgent", DropdownFilter),
        ("is_verify", DropdownFilter),
        ("position", ChoiceDropdownFilter),
        ("experience", ChoiceDropdownFilter),
        ("academic_level", ChoiceDropdownFilter),
        ("type_of_workplace", ChoiceDropdownFilter),
        ("job_type", ChoiceDropdownFilter),
    ]
    ordering = ("id", 'job_name', "is_hot", "is_urgent", "is_verify", "views", "shares")
    list_per_page = 25


class SavedJobPostAdmin(admin.ModelAdmin):
    list_display = ("id", "job_post", "user")
    list_display_links = ("id", "job_post",)
    search_fields = ("job_post__job_name", "user__email")
    ordering = ("id",)
    list_per_page = 25


class JobPostActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "phone",
                    "job_post", "user", "resume",
                    "status")
    list_display_links = ("id",)
    search_fields = ("full_name", "email", "phone", "job_post__job_name")
    ordering = ("id", "full_name", "email", "status")
    list_filter = [
        ("status", ChoiceDropdownFilter),
    ]
    list_per_page = 25


admin.site.register(JobPost, JobPostAdmin)
admin.site.register(SavedJobPost, SavedJobPostAdmin)
admin.site.register(JobPostActivity, JobPostActivityAdmin)

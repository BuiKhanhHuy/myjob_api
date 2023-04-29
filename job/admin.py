from django.contrib import admin
from .models import (
    JobPost,
    SavedJobPost,
    JobPostActivity
)


class JobPostAdmin(admin.ModelAdmin):
    list_display = ("job_name", "career", "deadline", "quantity", "is_hot",
                    "is_urgent", "is_verify", "views", "shares")
    list_display_links = ("job_name",)
    list_editable = ("is_hot", "is_urgent", "is_verify")


class SavedJobPostAdmin(admin.ModelAdmin):
    list_display = ("job_post", "user")
    list_display_links = ("job_post",)


class JobPostActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "phone",
                    "job_post", "user", "resume",
                    "status")
    list_display_links = ("id",)


admin.site.register(JobPost, JobPostAdmin)
admin.site.register(SavedJobPost, SavedJobPostAdmin)
admin.site.register(JobPostActivity, JobPostActivityAdmin)

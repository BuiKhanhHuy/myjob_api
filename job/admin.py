from helpers import helper
from django.contrib import admin
from django import forms
from .models import (
    JobPost,
    SavedJobPost,
    JobPostActivity
)
from django_admin_listfilter_dropdown.filters import (RelatedDropdownFilter, DropdownFilter, ChoiceDropdownFilter)


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = '__all__'
        widgets = {
            'is_hot': forms.CheckboxInput(attrs={'class': "form-check-input"}),
            'is_urgent': forms.CheckboxInput(attrs={'class': "form-check-input"}),
        }


class JobPostActivityForm(forms.ModelForm):
    class Meta:
        model = JobPostActivity
        fields = '__all__'
        widgets = {
            'is_sent_email': forms.CheckboxInput(attrs={'class': "form-check-input"}),
            'is_deleted': forms.CheckboxInput(attrs={'class': "form-check-input"}),
        }


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ("id", "job_name", "career", "deadline", "quantity", "is_hot",
                    "is_urgent", "status", "views", "shares")
    list_display_links = ("id", "job_name",)
    list_editable = ("is_hot", "is_urgent")
    search_fields = ("job_name", "career__name")
    list_filter = [
        ("is_hot", DropdownFilter),
        ("is_urgent", DropdownFilter),
        ("status", ChoiceDropdownFilter),
        ("position", ChoiceDropdownFilter),
        ("experience", ChoiceDropdownFilter),
        ("academic_level", ChoiceDropdownFilter),
        ("type_of_workplace", ChoiceDropdownFilter),
        ("job_type", ChoiceDropdownFilter),
    ]
    ordering = ("id", 'job_name', "is_hot", "is_urgent", "status", "views", "shares")
    list_per_page = 25

    fields = ("job_name", "deadline", "quantity",
              "position", "type_of_workplace",
              "experience", "academic_level", "job_type",
              "salary_min", "salary_max",
              "contact_person_name", "contact_person_phone", "contact_person_email",
              "views", "shares", "career",
              "location", "user", "company",
              "gender_required", "job_description", "job_requirement", "benefits_enjoyed",
              "is_hot", "is_urgent", "status")

    readonly_fields = ('user', 'company')
    autocomplete_fields = ('career', 'location')
    list_select_related = ('career',)

    form = JobPostForm

    def save_model(self, request, obj, form, change):
        pre_status = None
        if change:
            job_post = JobPost.objects.filter(id=obj.id).first()
            if job_post:
                pre_status = job_post.status
        super().save_model(request, obj, form, change)
        if change:
            new_status = obj.status
            if pre_status != new_status:
                # send notification
                helper.add_job_post_verify_notification(obj)


@admin.register(SavedJobPost)
class SavedJobPostAdmin(admin.ModelAdmin):
    list_display = ("id", "job_post", "user")
    list_display_links = ("id", "job_post",)
    search_fields = ("job_post__job_name", "user__email")
    ordering = ("id",)
    list_per_page = 25

    readonly_fields = ('job_post', 'user')


@admin.register(JobPostActivity)
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
    readonly_fields = ('job_post', 'user', 'resume')

    form = JobPostActivityForm

"""
MyJob Recruitment System - Part of MyJob Platform

Author: Bui Khanh Huy
Email: khuy220@gmail.com
Copyright (c) 2023 Bui Khanh Huy

License: MIT License
See the LICENSE file in the project root for full license information.
"""

from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from kombu.utils.json import loads
from django import forms
from django.utils.html import mark_safe
from django_admin_listfilter_dropdown.filters import DropdownFilter, ChoiceDropdownFilter
from django.conf import settings
from django.db import transaction
from helpers import helper
from configs import variable_system as var_sys

from django_celery_beat.models import (
    IntervalSchedule,
    CrontabSchedule,
    PeriodicTask,
    SolarSchedule,
    ClockedSchedule
)
from django_celery_beat.admin import (
    TaskChoiceField, PeriodicTaskAdmin,
    CrontabScheduleAdmin,
    ClockedScheduleAdmin
)
from myjob_api.admin import custom_admin_site
from common.models import File
from .models import (
    Feedback,
    Banner
)
from helpers.cloudinary_service import CloudinaryService

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'


class BannerForm(forms.ModelForm):
    image_file = forms.FileField(required=False)
    image_mobile_file = forms.FileField(required=False)

    class Meta:
        model = Banner
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image_file'].required = False
        self.fields['image_mobile_file'].required = False


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "create_at", "content",
                    "rating", "is_active", "user")
    list_display_links = ("id",)
    list_editable = ("is_active",)
    search_fields = ("content",)
    list_filter = [
        ("create_at", DropdownFilter),
        ("rating", DropdownFilter),
        ("is_active", DropdownFilter),
    ]
    fields = (
        "content", "rating", "user", "is_active"
    )

    readonly_fields = ('user',)

    form = FeedbackForm


class BannerAdmin(admin.ModelAdmin):
    list_display = ("id", "show_image_url",
                    "show_mobile_image_url", "description",
                    "type", "platform", "is_active",
                    "is_show_button")
    list_display_links = ("id",)
    list_editable = ("is_show_button", "is_active")
    search_fields = ("description",)
    readonly_fields = ("show_image_url", "show_mobile_image_url")
    list_filter = [
        ("platform", ChoiceDropdownFilter),
        ("description_location", ChoiceDropdownFilter),
        ("is_show_button", DropdownFilter),
        ("is_active", DropdownFilter),
    ]
    fields = (
        "button_text", "button_link", "description",
        "description_location", "platform", "type",
        "show_image_url", "image_file",
        "show_mobile_image_url", "image_mobile_file",
        "is_show_button", "is_active"
    )

    def show_image_url(self, banner):
        if banner and banner.image:
            return mark_safe(
                r"""<img src='{0}'
                alt='background' style="border-radius: 5px; object-fit:cover;" width='220px' height='110px'/>""".format(
                    banner.image.get_full_url())
            )
        return "---"

    def show_mobile_image_url(self, banner):
        if banner and banner.image_mobile:
            return mark_safe(
                r"""<img src='{0}'
                alt='background' style="border-radius: 5px; object-fit:cover;" width='220px' height='110px'/>""".format(
                    banner.image_mobile.get_full_url())
            )
        return "---"

    show_image_url.short_description = "Web background image"
    show_mobile_image_url.short_description = "Mobile background image"

    form = BannerForm

    def save_model(self, request, banner, form, change):
        # Call the parent class's save_model method
        super().save_model(request, banner, form, change)

        # Get the uploaded image files
        image_file = request.FILES.get('image_file', None)
        image_mobile_file = request.FILES.get('image_mobile_file', None)

        # If a web banner image is uploaded
        if image_file:
            try:
                # Upload the image to cloudinary
                with transaction.atomic():
                    public_id = None
                    # Overwrite if image already exists
                    if banner.image:
                        path_list = banner.image.public_id.split('/')
                        public_id = path_list[-1] if path_list else None
                    # Upload
                    banner_image_upload_result = CloudinaryService.upload_image(
                        image_file,
                        settings.CLOUDINARY_DIRECTORY["web_banner"],
                        public_id
                    )
                    # Update or create file
                    banner.image = File.update_or_create_file_with_cloudinary(
                        banner.image,
                        banner_image_upload_result,
                        File.WEB_BANNER_TYPE
                    )
                    banner.save()
            except Exception as ex:
                helper.print_log_error("banner_image_save_model", ex)

        # If a mobile banner image is uploaded
        if image_mobile_file:
            try:
                # Upload the image to cloudinary
                with transaction.atomic():
                    public_id = None
                    # Overwrite if image already exists
                    if banner.image_mobile:
                        path_list = banner.image_mobile.public_id.split('/')
                        public_id = path_list[-1] if path_list else None
                    # Upload
                    banner_mobile_image_upload_result = CloudinaryService.upload_image(
                        image_mobile_file,
                        settings.CLOUDINARY_DIRECTORY["mobile_banner"],
                        public_id
                    )
                    # Update or create file
                    banner.image_mobile = File.update_or_create_file_with_cloudinary(
                        banner.image_mobile,
                        banner_mobile_image_upload_result,
                        File.MOBILE_BANNER_TYPE
                    )
                    banner.save()
            except Exception as ex:
                helper.print_log_error("banner_mobile_image_save_model", ex)

        # If a web banner or mobile banner image is uploaded, save the banner
        if image_file or image_mobile_file:
            banner.save()


class CustomPeriodicTaskForm(forms.ModelForm):
    """Form that lets you create and modify periodic tasks."""

    regtask = TaskChoiceField(
        label=_('Task (registered)'),
        required=False,
    )
    task = forms.CharField(
        label=_('Task (custom)'),
        required=False,
        max_length=200,
    )

    class Meta:
        """Form metadata."""

        model = PeriodicTask
        exclude = ()
        widgets = {
            'one_off': forms.CheckboxInput(attrs={'class': "form-check-input"}),
            'enabled': forms.CheckboxInput(attrs={'class': "form-check-input"}),
        }

    def clean(self):
        data = super().clean()
        regtask = data.get('regtask')
        if regtask:
            data['task'] = regtask
        if not data['task']:
            exc = forms.ValidationError(_('Need name of task'))
            self._errors['task'] = self.error_class(exc.messages)
            raise exc

        if data.get('expire_seconds') is not None and data.get('expires'):
            raise forms.ValidationError(
                _('Only one can be set, in expires and expire_seconds')
            )
        return data

    def _clean_json(self, field):
        value = self.cleaned_data[field]
        try:
            loads(value)
        except ValueError as exc:
            raise forms.ValidationError(
                _('Unable to parse JSON: %s') % exc,
            )
        return value

    def clean_args(self):
        return self._clean_json('args')

    def clean_kwargs(self):
        return self._clean_json('kwargs')


class CustomPeriodicTaskAdmin(PeriodicTaskAdmin):
    form = CustomPeriodicTaskForm
    fieldsets = (
        (None, {
            'fields': ('name', 'regtask', 'task', 'enabled', 'description',),
            'classes': ('extrapretty', 'wide'),
        }),
        (_('Schedule'), {
            'fields': ('interval', 'crontab', 'crontab_translation', 'solar',
                       'clocked', 'start_time', 'last_run_at', 'one_off'),
            'classes': ('extrapretty', 'wide'),
        }),
        (_('Arguments'), {
            'fields': ('args', 'kwargs'),
            'classes': ('extrapretty', 'wide'),
        }),
        (_('Execution Options'), {
            'fields': ('expires', 'expire_seconds', 'queue', 'exchange',
                       'routing_key', 'priority', 'headers'),
            'classes': ('extrapretty', 'wide'),
        }),
    )


class IntervalScheduleAdmin(admin.ModelAdmin):
    """Admin class for IntervalSchedule"""
    list_display = ('every', 'period')
    list_filter = ('period',)
    search_fields = ('every',)


class SolarScheduleAdmin(admin.ModelAdmin):
    """Admin class for SolarSchedule"""
    list_display = ('event', 'latitude', 'longitude')
    search_fields = ('event', 'latitude', 'longitude')


admin.site.unregister(PeriodicTask)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(ClockedSchedule)
custom_admin_site.register(Feedback, FeedbackAdmin)
custom_admin_site.register(Banner, BannerAdmin)
custom_admin_site.register(IntervalSchedule, IntervalScheduleAdmin)
custom_admin_site.register(CrontabSchedule, CrontabScheduleAdmin)
custom_admin_site.register(SolarSchedule, SolarScheduleAdmin)
custom_admin_site.register(ClockedSchedule, ClockedScheduleAdmin)
custom_admin_site.register(PeriodicTask, CustomPeriodicTaskAdmin)

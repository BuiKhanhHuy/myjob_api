import cloudinary.uploader
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from kombu.utils.json import loads
from django import forms
from django.utils.html import mark_safe
from django_admin_listfilter_dropdown.filters import DropdownFilter, ChoiceDropdownFilter
from django.conf import settings
from helpers import helper

from django_celery_beat.models import (
    PeriodicTask
)
from django_celery_beat.admin import (
    TaskChoiceField, PeriodicTaskAdmin
)

from .models import (
    Feedback,
    Banner
)


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': "form-check-input"}),
        }


class BannerForm(forms.ModelForm):
    image_file = forms.FileField(required=False)
    image_mobile_file = forms.FileField(required=False)

    class Meta:
        model = Banner
        fields = '__all__'
        widgets = {
            'button_link': forms.URLInput(attrs={'class': "form-control"}),
            'is_show_button': forms.CheckboxInput(attrs={'class': "form-check-input"}),
            'is_active': forms.CheckboxInput(attrs={'class': "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image_file'].required = False
        self.fields['image_mobile_file'].required = False


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "create_at", "content", "rating", "is_active", "user")
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


@admin.register(Banner)
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
        if banner and banner.image_url:
            return mark_safe(
                r"""<img src='{0}'
                alt='background' style="border-radius: 5px; object-fit:cover;" width='220px' height='110px'/>""".format(
                    banner.image_url)
            )
        return "---"

    def show_mobile_image_url(self, banner):
        if banner and banner.image_mobile_url:
            return mark_safe(
                r"""<img src='{0}'
                alt='background' style="border-radius: 5px; object-fit:cover;" width='220px' height='110px'/>""".format(
                    banner.image_mobile_url)
            )
        return "---"

    show_image_url.short_description = "Web background image"
    show_mobile_image_url.short_description = "Mobile background image"

    form = BannerForm

    def save_model(self, request, banner, form, change):
        super().save_model(request, banner, form, change)

        image_file = request.FILES.get('image_file', None)
        image_mobile_file = request.FILES.get('image_mobile_file', None)

        if image_file:
            try:
                banner_image_upload_result = cloudinary.uploader.upload(
                    image_file,
                    folder=settings.CLOUDINARY_DIRECTORY[
                        "webBanner"],
                    public_id=banner.id
                )
                banner_image_url = banner_image_upload_result.get('secure_url')
            except Exception as ex:
                helper.print_log_error("banner_image_save_model", ex)
            else:
                banner.image_url = banner_image_url

        if image_mobile_file:
            try:
                banner_mobile_image_upload_result = cloudinary.uploader.upload(
                    image_mobile_file,
                    folder=settings.CLOUDINARY_DIRECTORY[
                        "mobileBanner"],
                    public_id=banner.id
                )
                banner_mobile_image_url = banner_mobile_image_upload_result.get('secure_url')
            except Exception as ex:
                helper.print_log_error("banner_mobile_image_save_model", ex)
            else:
                banner.image_mobile_url = banner_mobile_image_url

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


admin.site.unregister(PeriodicTask)
admin.site.register(PeriodicTask, CustomPeriodicTaskAdmin)

"""
MyJob Recruitment System - Part of MyJob Platform

Author: Bui Khanh Huy
Email: khuy220@gmail.com
Copyright (c) 2023 Bui Khanh Huy

License: MIT License
See the LICENSE file in the project root for full license information.
"""

from django.contrib import admin
from django.utils.html import mark_safe
from django import forms
from django.conf import settings
from django.db import transaction
from helpers import helper
from configs import variable_system as var_sys
from myjob_api.admin import custom_admin_site
from .models import (
    City,
    District,
    Location,
    Career,
    File
)
from django_admin_listfilter_dropdown.filters import (RelatedDropdownFilter)
from helpers.cloudinary_service import CloudinaryService


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'


class CareerForm(forms.ModelForm):
    icon_file = forms.FileField(required=False)

    class Meta:
        model = Career
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['icon_file'].required = False


class LocationInlineAdmin(admin.StackedInline):
    model = Location
    extra = 1


class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    search_fields = ("name",)
    list_display_links = ("id", "name",)
    ordering = ("id", 'name',)
    list_per_page = 25


class DistrictAdmin(admin.ModelAdmin):
    list_display = ("id", "name", 'city')
    list_display_links = ("id", "name",)
    search_fields = ("name",)
    readonly_fields = ('city',)
    ordering = ("id", 'name',)
    list_per_page = 25

    autocomplete_fields = ('city',)
    list_select_related = ('city',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "city", 'district', 'lat', 'lng', 'address')
    list_display_links = ("id", "city",)
    search_fields = ("address", "city__name", "district__name")
    list_filter = [
        ("city", RelatedDropdownFilter),
        ("district", RelatedDropdownFilter),
    ]
    ordering = ("id", 'address',)
    list_per_page = 25

    autocomplete_fields = ('city', 'district')
    list_select_related = ('city',)

    form = LocationForm


class CareerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "show_icon", "app_icon_name")
    list_display_links = ("id", "name",)
    search_fields = ("name",)
    ordering = ("id", 'name',)
    readonly_fields = ("show_icon",)
    list_per_page = 25

    fields = ('name', 'show_icon', 'icon_file')

    def show_icon(self, career):
        if career:
            return mark_safe(
                r"""<img src='{0}'
                alt='{1}' width='50px' height='50px' style="object-fit:contain;"/>""".format(
                    career.icon.get_full_url() if career.icon else var_sys.NO_IMAGE,
                    career.name)
            )

    show_icon.short_description = "Icon"

    form = CareerForm

    def save_model(self, request, career, form, change):
        super().save_model(request, career, form, change)
        icon_file = request.FILES.get("icon_file", None)
        if icon_file:
            try:
                with transaction.atomic():
                    public_id = None
                    # Overwrite if image already exists
                    if career.icon:
                        path_list = career.icon.public_id.split('/')
                        public_id = path_list[-1] if path_list else None
                    # Upload
                    career_image_upload_result = CloudinaryService.upload_image(
                        icon_file,
                        folder=settings.CLOUDINARY_DIRECTORY["career_image"],
                        public_id=public_id
                    )
                    
                    # Update or create file
                    career.icon = File.update_or_create_file_with_cloudinary(
                        career.icon,
                        career_image_upload_result,
                        File.CAREER_IMAGE_TYPE
                    )
                    career.save()
            except Exception as ex:
                helper.print_log_error("career_image_save_model", ex)


custom_admin_site.register(City, CityAdmin)
custom_admin_site.register(District, DistrictAdmin)
custom_admin_site.register(Location, LocationAdmin)
custom_admin_site.register(Career, CareerAdmin)

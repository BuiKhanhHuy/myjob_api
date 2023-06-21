import cloudinary.uploader
from django.contrib import admin
from django.utils.html import mark_safe
from django import forms
from django.conf import settings
from helpers import helper
from .models import (
    City,
    District,
    Location,
    Career
)
from django_admin_listfilter_dropdown.filters import (RelatedDropdownFilter)


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
        widgets = {
            'lat': forms.NumberInput(attrs={'class': "form-control"}),
            'lng': forms.NumberInput(attrs={'class': "form-control"}),
        }


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

    form = LocationForm


class CareerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "show_icon", "app_icon_name")
    list_display_links = ("id", "name",)
    search_fields = ("name", )
    ordering = ("id", 'name',)
    readonly_fields = ("show_icon",)
    list_per_page = 25

    fields = ('name', 'show_icon', 'icon_file')

    def show_icon(self, career):
        if career:
            return mark_safe(
                r"""<img src='{0}'
                alt='{1}' width='50px' height='50px' style="object-fit:contain;"/>""".format(career.icon_url,
                                                                                             career.name)
            )

    show_icon.short_description = "Icon"

    form = CareerForm

    def save_model(self, request, career, form, change):
        super().save_model(request, career, form, change)
        icon_file = request.FILES.get("icon_file", None)
        if icon_file:
            try:
                career_image_upload_result = cloudinary.uploader.upload(
                    icon_file,
                    folder=settings.CLOUDINARY_DIRECTORY[
                        "careerImage"],
                    public_id=career.id
                )
                career_image_url = career_image_upload_result.get('secure_url')
            except Exception as ex:
                helper.print_log_error("career_image_save_model", ex)
            else:
                career.icon_url = career_image_url
                career.save()


admin.site.register(Career, CareerAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Location, LocationAdmin)

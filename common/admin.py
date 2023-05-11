from django.contrib import admin
from django.utils.html import mark_safe
from .models import (
    City,
    District,
    Location,
    Career
)
from django_admin_listfilter_dropdown.filters import (RelatedDropdownFilter)


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


class CareerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "show_icon")
    list_display_links = ("id", "name",)
    search_fields = ("name", )
    ordering = ("id", 'name',)
    readonly_fields = ("icon_url",)
    list_per_page = 25

    def show_icon(self, career):
        if career:
            return mark_safe(
                r"""<img src='{0}'
                alt='{1}' width='30px' height='30px'/>""".format(career.icon_url,
                                                                 career.name)
            )

    show_icon.short_description = "Icon"


admin.site.register(Career, CareerAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Location, LocationAdmin)
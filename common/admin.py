from django.contrib import admin
from django.utils.html import mark_safe
from .models import (
    City,
    District,
    Location,
    Career
)


class LocationInlineAdmin(admin.StackedInline):
    model = Location
    # classes = ('collapse',)
    # fk_name = 'job_seeker_profile'
    # form = forms.CareerGoalForm
    extra = 1


class CityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_display_links = ("name",)


class DistrictAdmin(admin.ModelAdmin):
    list_display = ("name", 'city')
    list_display_links = ("name",)
    readonly_fields = ('city',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ("city", 'district', 'lat', 'lng', 'address')
    list_display_links = ("city",)


class CareerAdmin(admin.ModelAdmin):
    list_display = ("name", "show_icon")
    list_display_links = ("name",)
    readonly_fields = ("icon_url",)

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
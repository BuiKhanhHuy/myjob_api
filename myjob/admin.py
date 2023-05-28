from django.contrib import admin
from django.utils.html import mark_safe
from django_admin_listfilter_dropdown.filters import DropdownFilter, ChoiceDropdownFilter

from .models import (
    Feedback,
    Banner
)


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


class BannerAdmin(admin.ModelAdmin):
    list_display = ("id", "description",  "is_active",
                    "is_show_button", "show_image_url", "show_mobile_image_url", "type", "platform")
    list_display_links = ("id",)
    list_editable = ("is_show_button", "is_active")
    search_fields = ("description",)
    list_filter = [
        ("platform", ChoiceDropdownFilter),
        ("description_location", ChoiceDropdownFilter),
        ("is_show_button", DropdownFilter),
        ("is_active", DropdownFilter),
    ]

    def show_image_url(self, banner):
        if banner and banner.image_url:
            return mark_safe(
                r"""<img src='{0}'
                alt='background' style="border-radius: 5px;" width='220px' height='110px'/>""".format(banner.image_url)
            )
        return "---"

    def show_mobile_image_url(self, banner):
        if banner and banner.image_mobile_url:
            return mark_safe(
                r"""<img src='{0}'
                alt='background' style="border-radius: 5px;" width='220px' height='110px'/>""".format(
                    banner.image_mobile_url)
            )
        return "---"

    show_image_url.short_description = "Web background image"
    show_mobile_image_url.short_description = "Mobile background image"


admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Banner, BannerAdmin)

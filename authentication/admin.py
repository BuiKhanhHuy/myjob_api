from django.contrib import admin
from django.utils.html import mark_safe
from .models import (
    User,
    ForgotPasswordToken
)
from django_admin_listfilter_dropdown.filters import (DropdownFilter )


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "show_avatar", "email", "full_name", "is_verify_email", "is_active", "role_name")
    list_display_links = ("id", "show_avatar", "email")
    list_editable = ("is_active",)
    search_fields = ("full_name", "email")
    list_filter = [
        ("email", DropdownFilter),
        ("role_name", DropdownFilter),
        ("is_verify_email", DropdownFilter),
        ("is_active", DropdownFilter),
    ]
    ordering = ("id", "email", "full_name", "is_verify_email", "is_active", "role_name")
    readonly_fields = ("show_avatar", "avatar_public_id", "avatar_url", "password")
    list_per_page = 25

    def show_avatar(self, user):
        if user:
            return mark_safe(
                r"""<img src='{0}'
                alt='{1}' style="border-radius: 50px;" width='50px' height='50px'/>""".format(user.avatar_url,
                                                                                              user.full_name)
            )

    show_avatar.short_description = "Avatar"


class ForgotPasswordTokenAdmin(admin.ModelAdmin):
    list_display = ("id", "token", "code", "expired_at", "is_active", "platform", "user")
    list_display_links = ("id", "token", "code")
    search_fields = ("token", "code", "user__email")
    list_filter = [
        ("platform", DropdownFilter),
        ("is_active", DropdownFilter),
    ]
    ordering = ("id", "token", "code", "expired_at", "is_active", "platform")
    readonly_fields = ("token", "code", "expired_at", "is_active", "platform", "user")
    list_per_page = 25


admin.site.register(User, UserAdmin)
admin.site.register(ForgotPasswordToken, ForgotPasswordTokenAdmin)

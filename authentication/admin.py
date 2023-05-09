from django.contrib import admin
from django.utils.html import mark_safe
from .models import (
    User,
    ForgotPasswordToken
)


class UserAdmin(admin.ModelAdmin):
    list_display = ("show_avatar", "email", "full_name", "is_verify_email", "is_active", "role_name")
    list_display_links = ("show_avatar", "email")
    list_editable = ("is_active",)
    readonly_fields = ("show_avatar", "avatar_public_id", "avatar_url", "password")

    def show_avatar(self, user):
        if user:
            return mark_safe(
                r"""<img src='{0}'
                alt='{1}' style="border-radius: 50px;" width='50px' height='50px'/>""".format(user.avatar_url,
                                                                                              user.full_name)
            )

    show_avatar.short_description = "Avatar"


class ForgotPasswordTokenAdmin(admin.ModelAdmin):
    list_display = ("token", "code", "expired_at", "is_active", "platform", "user")
    list_display_links = ("token", "code")
    readonly_fields = ("token", "code", "expired_at", "is_active", "platform", "user")


admin.site.register(User, UserAdmin)
admin.site.register(ForgotPasswordToken, ForgotPasswordTokenAdmin)

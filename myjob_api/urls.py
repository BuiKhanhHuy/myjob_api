from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.contrib.auth import views as auth_views
from admin_volt import views as admin_volt_views
from myjob import admin_views

schema_view = get_schema_view(
    openapi.Info(
        title="MyJob API",
        default_version='v1',
        description="API hệ thống giới thiêu việc làm.",
        terms_of_service="",
        contact=openapi.Contact(email="huybk2@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('admin/', include(
        [
            # Index
            path('', admin_views.index, name="index"),
            path('notifications/', admin_views.myjob_notifications, name="myjob_notifications"),
            # Pages
            path('pages/dashboard/', admin_views.dashboard, name="dashboard"),
            path('pages/transaction/', admin_views.transaction, name="transaction"),
            path('pages/settings/', admin_views.settings, name="settings"),

            # Tables
            path('tables/bs-tables/', admin_views.bs_tables, name="bs_tables"),

            # Components
            path('components/buttons/', admin_views.buttons, name="buttons"),
            path('components/notifications/', admin_views.notifications, name="notifications"),
            path('components/forms/', admin_views.forms, name="forms"),
            path('components/modals/', admin_views.modals, name="modals"),
            path('components/typography/', admin_views.typography, name="typography"),

            # Authentication
            path('accounts/register/', admin_views.register_view, name="register"),
            path('accounts/login/', admin_volt_views.UserLoginView.as_view(), name="login"),
            path('accounts/logout/', admin_volt_views.logout_view, name="logout"),
            path('accounts/password-change/', admin_volt_views.UserPasswordChangeView.as_view(),
                 name='password_change'),
            path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
                template_name='accounts/password-change-done.html'
            ), name="password_change_done"),
            path('accounts/password-reset/', admin_volt_views.UserPasswordResetView.as_view(), name="password_reset"),
            path('accounts/password-reset-confirm/<uidb64>/<token>/',
                 admin_volt_views.UserPasswrodResetConfirmView.as_view(), name="password_reset_confirm"
                 ),
            path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
                template_name='accounts/password-reset-done.html'
            ), name='password_reset_done'),
            path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
                template_name='accounts/password-reset-complete.html'
            ), name='password_reset_complete'),

            path('accounts/lock/', admin_views.lock, name="lock"),

            # Errors
            path('error/404/', admin_volt_views.error_404, name="error_404"),
            path('error/500/', admin_volt_views.error_500, name="error_500"),

            # Extra
            path('pages/upgrade-to-pro/', admin_views.upgrade_to_pro, name="upgrade_to_pro"),

            path('api/', include([
                path('user-chart/', admin_views.user_chart),
                path('job-post-chart/', admin_views.job_post_chart),
                path('career-chart/', admin_views.career_chart),
                path('application-chart/', admin_views.application_chart),
            ]))
        ]
    )),
    path('admin/', admin.site.urls),
    path('api/', include(
        [
            path('common/', include('common.urls')),
            path('auth/', include('authentication.urls')),
            path('info/', include('info.urls')),
            path('job/', include('job.urls')),
            path('myjob/', include('myjob.urls')),
            path('chatbot/', include('chatbot.urls')),
        ]
    ))
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('token/', views.CustomTokenView.as_view()),
    path('', include('drf_social_oauth2.urls', namespace='drf')),
    path('email-exists/', views.check_email_exists),
    path('check-creds/', views.check_creds),
    path('verify-email/', views.verify_email),
    path('forgot-password/', views.forgot_password),
    path('reset-password/', views.reset_password),
    path('change-password/', views.change_password),
    path('update-user/', views.update_user_account),
    path('user-info/', views.get_user_info),
    path('job-seeker/register/', views.job_seeker_register),
    path('employer/register/', views.employer_register),
    # path('', include(router.urls))
]

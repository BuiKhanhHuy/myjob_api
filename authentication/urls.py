from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CustomTokenView,
    check_email_exists,
    reset_password,
    get_user_info,
    job_seeker_register,
    employer_register,
    UserViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('token/', CustomTokenView.as_view()),
    path('', include('drf_social_oauth2.urls', namespace='drf')),
    path('email-exists/', check_email_exists),
    path('reset-password', reset_password),
    path('user-info/', get_user_info),
    path('job-seeker/register/', job_seeker_register),
    path('employer/register/', employer_register),
    path('', include(router.urls))
]


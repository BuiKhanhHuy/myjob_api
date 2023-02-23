from django.urls import include, path
from .views.custom_token_views import CustomTokenView
from .views import auth_views

urlpatterns = [
    path('token/', CustomTokenView.as_view()),
    path('', include('drf_social_oauth2.urls', namespace='drf')),
    path('email-exists/', auth_views.check_email_exists),
    path('reset-password', auth_views.reset_password),
    path('job-seeker/', include([
        path('register/', auth_views.job_seeker_register),
    ])),
    path('employer/', include([
        path('register/', auth_views.employer_register),
    ]))
]

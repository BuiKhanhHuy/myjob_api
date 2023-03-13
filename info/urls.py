from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import web_views, app_views

app_router = DefaultRouter()

web_router = DefaultRouter()
web_router.register(r'job-seeker-profiles', web_views.JobSeekerProfileViewSet, basename='job-seeker-profile')

urlpatterns = [
    path('app/', include([
        path('', include(app_router.urls))
    ])),
    path('web/', include([
        path("profile/", web_views.ProfileView.as_view({'get': 'get_profile_info', 'patch': 'update_profile_info'})),
        path("profile-detail/", web_views.ProfileView.as_view({'get': 'get_profile_info_detail'})),
        path("", include(web_router.urls))
    ]))
]

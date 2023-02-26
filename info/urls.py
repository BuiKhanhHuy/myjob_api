from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    JobSeekerProfileViewSet
)

router = DefaultRouter()
router.register(r'job-seeker-profiles', JobSeekerProfileViewSet, basename='job-seeker-profile')

urlpatterns = [
    path("", include(router.urls))
]

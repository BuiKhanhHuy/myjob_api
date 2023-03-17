from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import web_views, app_views

app_router = DefaultRouter()
# app_router.register('job-posts', app_views.JobPostViewSet, basename="job-posts")

web_router = DefaultRouter()
web_router.register('job-posts', web_views.JobPostViewSet, basename="web-job-posts")

urlpatterns = [
    # path('app/', include([
    #     path('', include(app_router.urls))
    # ])),
    path('web/', include([
        path('', include(web_router.urls))
    ]))
]

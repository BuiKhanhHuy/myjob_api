from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import web_views, app_views

app_router = DefaultRouter()
app_router.register('job-posts', app_views.JobPostViewSet, basename="app-job-posts")
app_router.register('job-seeker-job-posts-activity', app_views.JobSeekerJobPostActivityViewSet,
                    basename='app-job-seeker-job-posts-activity')


web_router = DefaultRouter()
web_router.register('private-job-posts', web_views.PrivateJobPostViewSet, basename='private-web-job-posts')
web_router.register('job-posts', web_views.JobPostViewSet, basename="web-job-posts")
web_router.register('job-seeker-job-posts-activity', web_views.JobSeekerJobPostActivityViewSet,
                    basename='web-job-seeker-job-posts-activity')
web_router.register('employer-job-posts-activity', web_views.EmployerJobPostActivityViewSet,
                    basename='web-employer-job-posts-activity')

urlpatterns = [
    path('app/', include([
        path('', include(app_router.urls))
    ])),
    path('web/', include([
        path('', include(web_router.urls))
    ]))
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import web_views, app_views

app_router = DefaultRouter()
app_router.register('job-posts', app_views.JobPostViewSet, basename="app-job-posts")
app_router.register('job-seeker-job-posts-activity', app_views.JobSeekerJobPostActivityViewSet,
                    basename='app-job-seeker-job-posts-activity')
app_router.register('job-post-notifications', app_views.JobPostNotificationViewSet,
                    basename='app-job-post-notifications')

web_router = DefaultRouter()
web_router.register('private-job-posts', web_views.PrivateJobPostViewSet, basename='private-web-job-posts')
web_router.register('job-posts', web_views.JobPostViewSet, basename="web-job-posts")
web_router.register('job-seeker-job-posts-activity', web_views.JobSeekerJobPostActivityViewSet,
                    basename='web-job-seeker-job-posts-activity')
web_router.register('employer-job-posts-activity', web_views.EmployerJobPostActivityViewSet,
                    basename='web-employer-job-posts-activity')
web_router.register('job-post-notifications', web_views.JobPostNotificationViewSet,
                    basename='web-job-post-notifications')

urlpatterns = [
    path('app/', include([
        path('', include(app_router.urls))
    ])),
    path('web/', include([
        path('', include(web_router.urls)),
        path('statistics/', include([
            path('employer-general-statistics/', web_views.EmployerStatisticViewSet.as_view({
                'get': 'general_statistics',
            })),
            path('employer-recruitment-statistics/', web_views.EmployerStatisticViewSet.as_view({
                'post': 'recruitment_statistics',
            })),
            path('employer-candidate-statistics/', web_views.EmployerStatisticViewSet.as_view({
                'post': 'candidate_statistics',
            })),
            path('employer-application-statistics/', web_views.EmployerStatisticViewSet.as_view({
                'post': 'application_statistics',
            })),
            path('employer-recruitment-statistics-by-rank/', web_views.EmployerStatisticViewSet.as_view({
                'post': 'recruitment_statistics_by_rank',
            })),

            path('job-seeker-general-statistics/', web_views.JobSeekerStatisticViewSet.as_view({
                'get': 'general_statistics',
            })),
            path('job-seeker-total-view/', web_views.JobSeekerStatisticViewSet.as_view({
                'get': 'total_view',
            })),
            path('job-seeker-activity-statistics/', web_views.JobSeekerStatisticViewSet.as_view({
                'get': 'activity_statistics',
            })),
        ])),
    ]))
]

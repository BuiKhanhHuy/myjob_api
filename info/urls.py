from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import web_views, app_views, views

app_router = DefaultRouter()
app_router.register(r'job-seeker-profiles', app_views.JobSeekerProfileViewSet, basename='app-job-seeker-profile')
app_router.register(r'private-resumes', app_views.PrivateResumeViewSet, basename='app-private-resume')
app_router.register(r'experiences-detail', app_views.ExperienceDetailViewSet, basename='app-experience-detail')
app_router.register(r'educations-detail', app_views.EducationDetailViewSet, basename='app-education-detail')
app_router.register(r'certificates-detail', app_views.CertificateDetailViewSet, basename='app-certificate-detail')
app_router.register(r'language-skills', app_views.LanguageSkillViewSet, basename='app-language-skill')
app_router.register(r'advanced-skills', app_views.AdvancedSkillViewSet, basename='app-advanced-skill')
app_router.register(r'companies', app_views.CompanyViewSet, basename='app-company')

web_router = DefaultRouter()
web_router.register(r'job-seeker-profiles', web_views.JobSeekerProfileViewSet, basename='web-job-seeker-profile')
web_router.register(r'private-resumes', web_views.PrivateResumeViewSet, basename='private-resume')
web_router.register(r'resumes', web_views.ResumeViewSet, basename='resume')
web_router.register(r'resumes-saved', web_views.ResumeSavedViewSet, basename='resume-saved')
web_router.register(r'experiences-detail', web_views.ExperienceDetailViewSet, basename='experience-detail')
web_router.register(r'educations-detail', web_views.EducationDetailViewSet, basename='education-detail')
web_router.register(r'certificates-detail', web_views.CertificateDetailViewSet, basename='certificate-detail')
web_router.register(r'language-skills', web_views.LanguageSkillViewSet, basename='language-skill')
web_router.register(r'advanced-skills', web_views.AdvancedSkillViewSet, basename='advanced-skill')

web_router.register(r'private-companies', web_views.PrivateCompanyViewSet, basename='private-company')
web_router.register(r'companies', web_views.CompanyViewSet, basename='web-company')
web_router.register(r'company-images', web_views.CompanyImageViewSet, basename='company-image')

urlpatterns = [
    path('', include([
        path("profile/", views.ProfileView.as_view({
            'get': 'get_profile_info',
            'put': 'update_profile_info'
        })),
    ])),
    path('app/', include([
        path('', include(app_router.urls)),
        path("resume-views/", app_views.ResumeViewedAPIView.as_view()),
        path("companies-follow/", app_views.CompanyFollowedAPIView.as_view()),
    ])),
    path('web/', include([
        path("company/", web_views.CompanyView.as_view({'get': 'get_company_info'})),
        path("company/job-posts/<int:pk>/", web_views.CompanyView.as_view({'get': 'get_job_post_detail'})),
        path("", include(web_router.urls)),
        path("resume-views/", web_views.ResumeViewedAPIView.as_view()),
        path("companies-follow/", web_views.CompanyFollowedAPIView.as_view()),
    ])),
]

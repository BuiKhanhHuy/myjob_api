from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import web_views

app_router = DefaultRouter()

web_router = DefaultRouter()
web_router.register(r'job-seeker-profiles', web_views.JobSeekerProfileViewSet, basename='job-seeker-profile')
web_router.register(r'private-resumes', web_views.PrivateResumeViewSet, basename='private-resume')
web_router.register(r'resumes', web_views.ResumeViewSet, basename='resume')
web_router.register(r'resumes-saved', web_views.ResumeSavedViewSet, basename='resume-saved')
web_router.register(r'experiences-detail', web_views.ExperienceDetailViewSet, basename='experience-detail')
web_router.register(r'educations-detail', web_views.EducationDetailViewSet, basename='education-detail')
web_router.register(r'certificates-detail', web_views.CertificateDetailViewSet, basename='certificate-detail')
web_router.register(r'language-skills', web_views.LanguageSkillViewSet, basename='language-skill')
web_router.register(r'advanced-skills', web_views.AdvancedSkillViewSet, basename='advanced-skill')

web_router.register(r'private-companies', web_views.PrivateCompanyViewSet, basename='private-company')
web_router.register(r'companies', web_views.CompanyViewSet, basename='company')
web_router.register(r'company-images', web_views.CompanyImageViewSet, basename='company-image')

urlpatterns = [
    path('app/', include([
        path('', include(app_router.urls))
    ])),
    path('web/', include([
        path("profile/", web_views.ProfileView.as_view({'get': 'get_profile_info', 'put': 'update_profile_info'})),
        path("company/", web_views.CompanyView.as_view({'get': 'get_company_info'})),
        path("company/job-posts/<int:pk>/", web_views.CompanyView.as_view({'get': 'get_job_post_detail'})),
        path("", include(web_router.urls)),
        path("resume-views/", web_views.ResumeViewedAPIView.as_view()),
        path("companies-follow/", web_views.CompanyFollowedAPIView.as_view()),
        path("email-reply-to-job-seeker/", web_views.send_email_reply_to_job_seeker)
    ]))
]

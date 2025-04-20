from django.urls import path
from . import views

urlpatterns = [
    path('jobseeker/webhook/', views.JobSeekerDialogFlowWebhookView.as_view()),
    path('employer/webhook/', views.EmployerDialogFlowWebhookView.as_view()),
]

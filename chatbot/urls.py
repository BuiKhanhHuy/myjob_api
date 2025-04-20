"""
MyJob Recruitment System - Part of MyJob Platform

Author: Bui Khanh Huy
Email: khuy220@gmail.com
Copyright (c) 2023 Bui Khanh Huy

License: MIT License
See the LICENSE file in the project root for full license information.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('jobseeker/webhook/', views.JobSeekerDialogFlowWebhookView.as_view()),
    path('employer/webhook/', views.EmployerDialogFlowWebhookView.as_view()),
]

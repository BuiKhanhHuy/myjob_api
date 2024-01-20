from django.urls import path
from . import views

urlpatterns = [
    path('webhook/', views.DialogFlowWebhookView.as_view()),
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

app_router = DefaultRouter()

web_router = DefaultRouter()
web_router.register(r'feedbacks', views.FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('', include([
        path('create-fake-databases/', views.create_fake_data),
        path('send-noti-demo/', views.send_notification_demo),
    ])),
    path('app/', include([
        path('', include(app_router.urls))
    ])),
    path('web/', include([
        path("", include(web_router.urls)),
        path("sms-download-app/", views.send_sms_download_app)
    ]))
]

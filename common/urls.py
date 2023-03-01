from django.urls import include, path
from . import views

urlpatterns = [
    path('configs/', views.get_all_config)
]

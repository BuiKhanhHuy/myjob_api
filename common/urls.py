from django.urls import path
from . import views


urlpatterns = [
    path('create-databases/', views.create_database),
    path('configs/', views.get_all_config),
    path('districts/', views.get_districts),
]

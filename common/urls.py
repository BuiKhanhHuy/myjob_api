from django.urls import path
from . import views

urlpatterns = [
    path('create-databases/', views.create_database),
    path('configs/', views.get_all_config),
    path('districts/', views.get_districts),
    path('top-careers/', views.get_top_10_careers),
    path('all-careers/', views.get_all_careers),
]

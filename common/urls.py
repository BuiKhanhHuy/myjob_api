from django.urls import path
from . import views

urlpatterns = [
    path('configs/', views.get_all_config),
    path('districts/', views.get_districts),
    path('top-careers/', views.get_top_10_careers),
    path('all-careers/', views.get_all_careers),
    path('health/', views.health_check, name='health_check'),
]

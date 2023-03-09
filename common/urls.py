from django.urls import include, path
from . import views

urlpatterns = [
    path('create-databases/', views.create_database),
    path('configs/', views.get_all_config)
]

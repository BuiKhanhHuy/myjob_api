from django.urls import include, path
from .views import demo_views, custom_token_views

urlpatterns = [
    path('token/', custom_token_views.CustomTokenView.as_view()),
    path('', include('drf_social_oauth2.urls', namespace='drf')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    path('job-seeker/', include([
        path('register/', demo_views.demo),
        path('app/', include([

        ])),
        path('web/', include([

        ]))
    ])),
    path('employer/', include([
        path('register/', demo_views.demo),
    ]))
]

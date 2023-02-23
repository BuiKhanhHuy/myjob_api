from django.urls import path, include

urlpatterns = [
    path('job-seeker/', include([
        path('app/', include([

        ])),
        path('web/', include([

        ]))
    ])),
    path('employer/', include([

    ]))
]

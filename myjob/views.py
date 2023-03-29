from configs import variable_system as var_sys, renderers
from configs import variable_response as var_res
from rest_framework import viewsets
from rest_framework import generics
from .models import (
    Feedback
)
from .serializers import (
    FeedbackSerializer
)


class FeedbackViewSet(viewsets.ViewSet,
                      generics.ListAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    renderer_classes = [renderers.MyJSONRenderer]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()
                                        .filter(is_active=True).order_by('-rating')[:10])

        serializer = self.get_serializer(queryset, many=True,
                                         fields=['id', 'content', 'rating', 'isActive', 'userDict'])
        return var_res.Response(serializer.data)

import json
from configs.variable_response import response_data
from console.jobs import queue_mail
from helpers import helper
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import (
    JobPost
)
from ..serializers.app_serializers import (
    JobPostListSerializer,
    JobPostDetailSerializer
)


class JobPostViewSet(viewsets.ViewSet,
                     generics.ListAPIView,
                     generics.RetrieveAPIView):
    queryset = JobPost.objects
    serializer_class = JobPostListSerializer

    def get_serializer_class(self):
        if self.action in ["retrieve"]:
            return JobPostDetailSerializer
        return self.serializer_class

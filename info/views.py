import json
from configs.variable_response import response_data
from helpers import helper
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import JobSeekerProfile
from .serializers import JobSeekerProfileSerializer


class JobSeekerProfileViewSet(viewsets.ViewSet,
                              generics.ListCreateAPIView,
                              generics.RetrieveUpdateDestroyAPIView):
    queryset = JobSeekerProfile.objects
    serializer_class = JobSeekerProfileSerializer

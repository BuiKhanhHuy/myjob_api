import json
from configs.variable_response import response_data
from console.jobs import queue_mail
from helpers import helper
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class JobPostViewSet(viewsets.ViewSet,
                     generics.ListAPIView,
                     generics.RetrieveAPIView):
    pass
from configs import variable_response as var_res, renderers
from helpers import helper
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework import permissions as perms_sys
from authentication import permissions as perms_custom
from rest_framework import status
from ..models import (
    JobPost
)
from ..serializers import (
    JobPostSerializer
)


class JobPostViewSet(viewsets.ViewSet,
                     generics.ListCreateAPIView,
                     generics.RetrieveUpdateDestroyAPIView):
    queryset = JobPost.objects
    serializer_class = JobPostSerializer
    renderer_classes = [renderers.MyJSONRenderer]
    permission_classes = [perms_sys.AllowAny()]

    def get_permissions(self):
        if self.action in ["create", "update",
                           "partial_update", "destroy"]:
            return [perms_custom.IsEmployerUser()]
        return self.permission_classes

    # def get_serializer_class(self):
    #     if self.action in ['update']:
    #         return JobPostSerializer(fields=["id"])
    #     return self.serializer_class



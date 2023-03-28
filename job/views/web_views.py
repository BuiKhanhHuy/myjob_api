from configs import variable_response as var_res, renderers, paginations
from helpers import helper
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework import permissions as perms_sys
from authentication import permissions as perms_custom
from rest_framework import status
from ..models import (
    JobPost
)
from ..filters import (
    JobPostFilter
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
    pagination_class = paginations.CustomPagination
    permission_classes = [perms_sys.AllowAny()]
    filterset_class = JobPostFilter
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        if self.action in ["create", "update",
                           "partial_update", "destroy"]:
            return [perms_custom.IsEmployerUser()]
        return self.permission_classes

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()
                                        .order_by('-id', 'update_at', 'create_at'))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, fields=[
                'id', 'slug', 'companyDict', "salaryMin", "salaryMax",
                'jobName', 'isHot', 'isUrgent', 'salary', 'city', 'deadline',
                'locationDict'
            ])
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return var_res.Response(serializer.data)

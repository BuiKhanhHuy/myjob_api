from configs import variable_response as var_res, renderers, paginations
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from helpers import helper
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions as perms_sys
from authentication import permissions as perms_custom
from rest_framework import status
from ..models import (
    Company,
    CompanyFollowed,
)
from ..filters import (
    CompanyFilter
)
from ..serializers import (
    CompanySerializer,
)


class CompanyViewSet(viewsets.ViewSet,
                     generics.ListAPIView,
                     generics.RetrieveAPIView):
    queryset = Company.objects
    serializer_class = CompanySerializer
    permission_classes = [perms_sys.AllowAny]
    renderer_classes = [renderers.MyJSONRenderer]
    pagination_class = paginations.CustomPagination
    filterset_class = CompanyFilter
    filter_backends = [DjangoFilterBackend]
    lookup_field = "slug"

    def get_permissions(self):
        if self.action in ["followed"]:
            return [perms_custom.IsJobSeekerUser()]
        return [perms_sys.AllowAny()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()
                                        .order_by('-id', 'update_at', 'create_at'))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, fields=[
                'id', 'companyName', 'companyImageUrl',
                'followNumber', 'jobPostNumber', 'isFollowed'
            ])
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return var_res.Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, fields=[
            'id', 'slug', 'taxCode', 'companyName',
            'employeeSize', 'fieldOperation', 'location',
            'since', 'companyEmail', 'companyPhone',
            'websiteUrl', 'facebookUrl', 'youtubeUrl',
            'linkedinUrl', 'description',
            'companyImageUrl', 'companyCoverImageUrl',
            'followNumber', 'isFollowed', 'companyImages'
        ])
        return Response(data=serializer.data)

    @action(methods=["get"], detail=False,
            url_path="top", url_name="companies-top")
    def get_top_companies(self, request):
        try:
            queryset = Company.objects.annotate(num_follow=Count('companyfollowed'),
                                                num_job_post=Count('job_posts')
                                                ) \
                           .exclude(Q(company_image_public_id__isnull=True)
                                    | Q(website_url__isnull=True)
                                    | Q(field_operation__isnull=True)
                                    | Q(employee_size__isnull=True)
                                    | Q(since__isnull=True)) \
                           .order_by('-num_follow', '-num_job_post')[:10]
            serializer = CompanySerializer(queryset, many=True,
                                           fields=[
                                               'id', 'slug', 'companyName', 'companyImageUrl'
                                           ])
        except Exception as ex:
            helper.print_log_error("get_top_companies", ex)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=serializer.data)

    @action(methods=["post"], detail=True,
            url_path="followed", url_name="followed")
    def followed(self, request, slug):
        is_followed = False
        companies_followed = CompanyFollowed.objects.filter(user=request.user, company=self.get_object())
        if companies_followed.exists():
            company_followed = companies_followed.first()
            company_followed.delete()
        else:
            CompanyFollowed.objects.create(
                user=request.user,
                company=self.get_object(),
            )
            is_followed = True
        return Response(data={
            "isFollowed": is_followed
        })

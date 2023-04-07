from configs import variable_response as var_res, renderers, paginations, table_export
from helpers import utils
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework import permissions as perms_sys
from authentication import permissions as perms_custom
from rest_framework.response import Response
from info.models import Resume
from ..models import (
    JobPost,
    SavedJobPost
)
from ..filters import (
    JobPostFilter,
    AliasedOrderingFilter
)
from ..serializers import (
    JobPostSerializer
)


class PrivateJobPostViewSet(viewsets.ViewSet,
                            generics.ListAPIView,
                            generics.CreateAPIView,
                            generics.UpdateAPIView,
                            generics.DestroyAPIView):
    queryset = JobPost.objects.annotate(
        applied_total=Count('peoples_applied'),
    )
    serializer_class = JobPostSerializer
    renderer_classes = [renderers.MyJSONRenderer]
    pagination_class = paginations.CustomPagination
    permission_classes = [perms_custom.JobPostOwnerPerms]
    filterset_class = JobPostFilter
    filter_backends = [DjangoFilterBackend, AliasedOrderingFilter]
    ordering_fields = (
        ('jobName', 'job_name'),
        ('createAt', 'create_at'),
        ('deadline', 'deadline'),
        ('viewedTotal', 'views'),
        ('appliedTotal', 'applied_total')
    )

    def get_permissions(self):
        if self.action in ["get_suggested_job_posts"]:
            return [perms_sys.IsAuthenticated()]
        return [perms_custom.JobPostOwnerPerms()]

    @action(methods=["get"], detail=False,
            url_path="suggested-job-posts", url_name="suggested-job-posts")
    def get_suggested_job_posts(self, request):
        resumes = Resume.objects.filter(is_active=True, user=request.user)
        if resumes.exists():
            resume = resumes.first()
            queryset = JobPost.objects.filter(is_verify=True)
            if resume.career:
                queryset = queryset.filter(career=resume.career)
            if resume.city:
                queryset = queryset.filter(location__city=resume.city)

            queryset = queryset.order_by("-create_at", "-update_at")
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
        return var_res.Response()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()
                                        .filter(user=request.user,
                                                company=request.user.company)
                                        .order_by('-id', 'update_at', 'create_at'))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, fields=[
                "id", "slug", "jobName", "createAt", "deadline",
                "appliedNumber", "views", "isUrgent", "isVerify"
            ])
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return var_res.Response(serializer.data)

    @action(methods=["get"], detail=False,
            url_path="export", url_name="job-posts-export")
    def export_job_posts(self, request):
        queryset = self.filter_queryset(self.get_queryset()
                                        .filter(is_verify=True, user=request.user,
                                                company=request.user.company)
                                        .order_by('-id', 'update_at', 'create_at'))
        serializer = self.get_serializer(queryset, many=True, fields=[
            "id", "jobName", "views",
            "createAt", "deadline", "appliedNumber"
        ])
        result_data = utils.convert_data_with_en_key_to_vn_kew(serializer.data, table_export.JOB_POSTS_EXPORT_FIELD)

        return Response(data=result_data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, fields=[
            "id", "jobName", "academicLevel", "deadline", "quantity",
            "genderRequired",
            "jobDescription", "jobRequirement", "benefitsEnjoyed",
            "career", 'isVerify',
            "position", "typeOfWorkplace", "experience",
            "jobType", "salaryMin", "salaryMax", "isUrgent",
            "contactPersonName", "contactPersonPhone",
            "contactPersonEmail",
            "location"])
        return Response(data=serializer.data)


class JobPostViewSet(viewsets.ViewSet,
                     generics.ListAPIView,
                     generics.RetrieveAPIView):
    queryset = JobPost.objects
    serializer_class = JobPostSerializer
    renderer_classes = [renderers.MyJSONRenderer]
    pagination_class = paginations.CustomPagination
    permission_classes = [perms_sys.AllowAny]
    filterset_class = JobPostFilter
    filter_backends = [DjangoFilterBackend]
    lookup_field = "slug"

    def get_permissions(self):
        if self.action in ["get_job_posts_saved",
                           "get_job_posts_applied",
                           "job_saved"]:
            return [perms_custom.IsJobSeekerUser()]
        return [perms_sys.AllowAny()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(is_verify=True)
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, fields=[
            'id', 'slug', 'jobName', 'deadline', 'quantity', 'genderRequired',
            'jobDescription', 'jobRequirement', 'benefitsEnjoyed', 'career',
            'position', 'typeOfWorkplace', 'experience', 'academicLevel',
            'jobType', 'salaryMin', 'salaryMax', 'contactPersonName',
            'contactPersonPhone', 'contactPersonEmail',
            'location', 'createAt',
            'isSaved', 'isApplied', 'companyDict', 'views'
        ])
        return Response(data=serializer.data)

    @action(methods=["get"], detail=False,
            url_path="job-posts-saved", url_name="job-posts-saved")
    def get_job_posts_saved(self, request):
        user = request.user
        queryset = user.saved_job_posts.filter(is_verify=True) \
            .order_by('update_at', 'create_at')

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

    @action(methods=["get"], detail=False,
            url_path="job-posts-applied", url_name="job-posts-applied")
    def get_job_posts_applied(self, request):
        return var_res.response_data()

    @action(methods=["post"], detail=True,
            url_path="job-saved", url_name="job-saved")
    def job_saved(self, request, slug):
        saved_job_posts = SavedJobPost.objects.filter(user=request.user, job_post=self.get_object())
        is_saved = False
        if saved_job_posts.exists():
            saved_job_post = saved_job_posts.first()

            saved_job_post.delete()
        else:
            SavedJobPost.objects.create(
                user=request.user,
                job_post=self.get_object()
            )
            is_saved = True
        return Response(data={
            "isSaved": is_saved
        })

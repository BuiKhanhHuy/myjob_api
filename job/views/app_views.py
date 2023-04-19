from configs import variable_response as var_res, renderers, paginations
from helpers import helper
from django.db.models import Count, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework import permissions as perms_sys
from authentication import permissions as perms_custom
from rest_framework.response import Response
from rest_framework import status
from info.models import Resume
from ..models import (
    JobPost,
    SavedJobPost,
    JobPostActivity
)
from ..filters import (
    JobPostFilter,
)
from ..serializers import (
    JobPostSerializer,
    JobPostAroundFilterSerializer,
    JobPostAroundSerializer,
    JobSeekerJobPostActivitySerializer,
)


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

    def get_permissions(self):
        if self.action in ["get_job_posts_saved",
                           "get_job_posts_applied",
                           "job_saved",
                           "get_suggested_job_posts"]:
            return [perms_custom.IsJobSeekerUser()]
        return [perms_sys.AllowAny()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(is_verify=True)
                                        .order_by('-id', 'update_at', 'create_at'))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, fields=[
                'id', 'companyDict', "salaryMin", "salaryMax",
                'jobName', 'isHot', 'isUrgent',
                'career', 'position', 'experience', 'academicLevel',
                'city', 'jobType', 'typeOfWorkplace', 'deadline',
                'locationDict', 'updateAt', 'isSaved'
            ])
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return var_res.Response(serializer.data)

    @action(methods=["get"], detail=False,
            url_path="suggested-job-posts", url_name="suggested-job-posts")
    def get_suggested_job_posts(self, request):
        resumes = Resume.objects.filter(user=request.user) \
            .values_list("career", "city")
        careers_id = [x[0] for x in resumes]
        cities_id = [x[1] for x in resumes]

        queryset = JobPost.objects.filter(is_verify=True) \
            .filter(career__in=careers_id, location__city__in=cities_id)

        queryset = queryset.order_by("-create_at", "-update_at")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, fields=[
                'id', 'companyDict', "salaryMin", "salaryMax",
                'jobName', 'isHot', 'isUrgent',
                'career', 'position', 'experience', 'academicLevel',
                'city', 'jobType', 'typeOfWorkplace', 'deadline',
                'locationDict', 'updateAt', 'isSaved'
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
            'isSaved', 'isApplied', 'mobileCompanyDict', 'views'
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
                'id', 'companyDict', "salaryMin", "salaryMax",
                'jobName', 'isHot', 'isUrgent',
                'career', 'position', 'experience', 'academicLevel',
                'city', 'jobType', 'typeOfWorkplace', 'deadline',
                'locationDict', 'updateAt', 'isSaved'
            ])
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return var_res.Response(serializer.data)

    @action(methods=["post"], detail=True,
            url_path="job-saved", url_name="job-saved")
    def job_saved(self, request, pk):
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

    @action(methods=["get"], detail=False,
            url_path="count-job-posts-by-job-type", url_name="count-job-posts-by-job-type")
    def count_job_posts_by_job_type(self, request):
        try:
            data = JobPost.objects.values(typeOfWorkplace=F('type_of_workplace')).annotate(total=Count('id')).order_by()
        except Exception as ex:
            helper.print_log_error("count_job_posts_by_job_type", ex)
            return var_res.Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return var_res.Response(data=data)

    @action(methods=["post"], detail=False,
            url_path="job-posts-around", url_name="job-posts-around")
    def get_job_posts_around(self, request):
        data = request.data
        filter_serializer = JobPostAroundFilterSerializer(data=data)
        if not filter_serializer.is_valid():
            print(">> BAD REQUEST >> get_job_posts_around: ", filter_serializer.errors)
            return var_res.Response(status=status.HTTP_400_BAD_REQUEST)

        queryset = JobPost.objects.filter(is_verify=True)
        serializer = JobPostAroundSerializer(queryset, many=True)

        return var_res.Response(data=serializer.data)


class JobSeekerJobPostActivityViewSet(viewsets.ViewSet,
                                      generics.ListAPIView,
                                      generics.CreateAPIView):
    queryset = JobPostActivity.objects
    serializer_class = JobSeekerJobPostActivitySerializer
    permission_classes = [perms_custom.IsJobSeekerUser]
    renderer_classes = [renderers.MyJSONRenderer]
    pagination_class = paginations.CustomPagination

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = user.jobpostactivity_set \
            .order_by('-create_at', '-update_at')

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True, fields=[
                "id", "createAt", "mobileJobPostDict", "resumeDict"
            ])
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return var_res.Response(serializer.data)

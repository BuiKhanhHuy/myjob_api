import datetime

from configs import variable_response as var_res, renderers, paginations
from helpers import helper
from django.db.models import F, Count
from django.db.models.functions import ACos, Cos, Radians, Sin
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
    JobPostActivity,
    JobPostNotification
)
from ..filters import (
    JobPostFilter,
)
from ..serializers import (
    JobPostSerializer,
    JobPostAroundFilterSerializer,
    JobPostAroundSerializer,
    JobSeekerJobPostActivitySerializer,
    JobPostNotificationSerializer
)


class JobPostViewSet(viewsets.ViewSet,
                     generics.ListAPIView,
                     generics.RetrieveAPIView):
    queryset = JobPost.objects.all()
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
        queryset = self.filter_queryset(self.get_queryset().filter(is_verify=True,
                                                                   deadline__gte=datetime.datetime.now().date())
                                        .order_by('-create_at', '-update_at'))

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
        filter_data = filter_serializer.data
        # latitude truyền vào
        lat = filter_data.get('currentLatitude')
        # longitude truyền vào
        lng = filter_data.get('currentLongitude')
        # bán kính truyền vào (đơn vị km)
        radius = filter_data.get("radius")

        # Chuyển đổi vị trí truyền vào thành radian
        lat_radian = Radians(lat)
        lng_radian = Radians(lng)

        # Tính toán khoảng cách và filter các dòng thỏa mãn
        queryset = self.filter_queryset(self.get_queryset().annotate(
            lat_radian=Radians('location__lat'),
            lng_radian=Radians('location__lng'),
            cos_lat_radian=Cos(Radians('location__lat')),
            sin_lat_radian=Sin(Radians('location__lat')),
            cos_lng_radian=Cos(Radians('location__lng')),
            sin_lng_radian=Sin(Radians('location__lng')),
            distance=6367.0 * ACos(
                Cos(lat_radian) * F('cos_lat_radian') * Cos(lng_radian - F('lng_radian')) +
                Sin(lat_radian) * F('sin_lat_radian')
            )
        ).filter(distance__lte=radius).order_by('update_at', 'create_at'))

        is_pagination = request.query_params.get("isPagination", None)

        if is_pagination and is_pagination == "OK":
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = JobPostAroundSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = JobPostAroundSerializer(queryset, many=True)
        return var_res.Response(serializer.data)


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


class JobPostNotificationViewSet(viewsets.ViewSet,
                                 generics.CreateAPIView,
                                 generics.ListAPIView,
                                 generics.UpdateAPIView,
                                 generics.DestroyAPIView):
    queryset = JobPostNotification.objects.all()
    serializer_class = JobPostNotificationSerializer
    renderer_classes = [renderers.MyJSONRenderer]
    pagination_class = paginations.CustomPagination
    permission_classes = [perms_custom.IsJobSeekerUser]

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = self.get_queryset().filter(user=user).order_by('-is_active', '-update_at')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, fields=[
                "id", "jobName", "position", "experience", "salary",
                "frequency", "isActive", "career", "city"
            ])
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return var_res.Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, fields=[
            "id", "jobName", "position", "experience",
            "salary", "frequency", "career", "city"
        ])
        return Response(data=serializer.data)

    @action(methods=["put"], detail=True,
            url_path='active', url_name="active", )
    def active_job_post_notification(self, request, pk):
        user = request.user
        job_post_notification = self.get_object()

        if job_post_notification.is_active:
            job_post_notification.is_active = False
            job_post_notification.save()
        else:
            if JobPostNotification.objects.filter(user=user, is_active=True).count() >= 3:
                return var_res.Response(status=status.HTTP_400_BAD_REQUEST,
                                        data={"errorMessage": ["Tối đa 3 thông báo việc làm được bật"]})
            job_post_notification.is_active = True
            job_post_notification.save()

        is_active = job_post_notification.is_active
        return var_res.Response(data={
            "isActive": is_active
        })

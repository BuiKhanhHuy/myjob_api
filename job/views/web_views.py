import datetime
import calendar
import pandas as pd
from datetime import timedelta
from console.jobs import queue_mail
from configs import variable_response as var_res, variable_system as var_sys, \
    renderers, paginations, table_export
from helpers import utils, helper
from django.conf import settings
from django.db.models import Count, F, Q, Sum
from django.db.models.functions import TruncDate, ExtractYear, ExtractMonth, TruncMonth, TruncYear
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
    AliasedOrderingFilter,
    EmployerJobPostActivityFilter
)
from ..serializers import (
    JobPostSerializer,
    JobSeekerJobPostActivitySerializer,
    EmployerJobPostActivitySerializer,
    EmployerJobPostActivityExportSerializer,
    JobPostNotificationSerializer,
    StatisticsSerializer
)
from info.models import (
    ResumeViewed,
    CompanyFollowed
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
            url_path="job-posts-options", url_name="job-posts-options")
    def get_job_post_options(self, request):
        user = request.user
        queryset = self.queryset.filter(user=user, company=user.company)

        serializer = JobPostSerializer(queryset, many=True,
                                       fields=[
                                           "id",
                                           "jobName"
                                       ])
        return var_res.Response(serializer.data)

    @action(methods=["get"], detail=False,
            url_path="suggested-job-posts", url_name="suggested-job-posts")
    def get_suggested_job_posts(self, request):
        resumes = Resume.objects.filter(user=request.user) \
            .values_list("career", "city")
        careers_id = [x[0] for x in resumes]
        cities_id = [x[1] for x in resumes]

        queryset = JobPost.objects.filter(is_verify=True, deadline__gte=datetime.datetime.now().date()) \
            .filter(career__in=careers_id, location__city__in=cities_id)

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # gui noti cho admin
        print("GỬI NOTI")
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        user = request.user

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        # gui noti yeu cau duyet bai
        helper.add_post_verify_required_notifications(
            company=user.company,
            job_post=self.get_object()
        )
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()
                                        .filter(user=request.user,
                                                company=request.user.company)
                                        .order_by('-update_at', '-create_at'))

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
                                        .order_by('update_at', 'create_at'))
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
        queryset = self.filter_queryset(self.get_queryset().filter(is_verify=True,
                                                                   deadline__gte=datetime.datetime.now().date())
                                        .order_by('-update_at', '-create_at'))

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
        try:
            instance.views = F('views') + 1
            instance.save()
            instance.refresh_from_db()
        except Exception as ex:
            helper.print_log_error("save views", ex)

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
                'jobName', 'isHot', 'isUrgent', 'isApplied', 'salary', 'city', 'deadline',
                'locationDict'
            ])
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return var_res.Response(serializer.data)

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
                "id", "createAt", "jobPostDict", "resumeDict"
            ])
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return var_res.Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job_post_activity = serializer.save()
        headers = self.get_success_headers(serializer.data)

        # send email here
        user = request.user
        job_post = job_post_activity.job_post
        company = job_post.company

        app_env = settings.APP_ENVIRONMENT
        domain = settings.DOMAIN_CLIENT[app_env]
        subject = f"Xác nhận ứng tuyển: {job_post.job_name}"
        to = [user.email]
        data = {
            "full_name": user.full_name,
            "company_name": company.company_name,
            "job_name": job_post.job_name,
            "find_job_post_link": domain + "viec-lam",
        }
        queue_mail.send_email_confirm_application.delay(
            to=to,
            subject=subject,
            data=data
        )
        # send noti
        helper.add_apply_job_notifications(
            job_post_activity=job_post_activity
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EmployerJobPostActivityViewSet(viewsets.ViewSet,
                                     generics.ListAPIView,
                                     generics.UpdateAPIView):
    queryset = JobPostActivity.objects
    serializer_class = EmployerJobPostActivitySerializer
    permission_classes = [perms_custom.IsEmployerUser]
    renderer_classes = [renderers.MyJSONRenderer]
    pagination_class = paginations.CustomPagination
    filterset_class = EmployerJobPostActivityFilter
    filter_backends = [DjangoFilterBackend]

    def list(self, request, *args, **kwargs):
        user = request.user

        queryset = self.filter_queryset(self.get_queryset().filter(job_post__company=user.company)
                                        .order_by('-id', 'create_at'))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, fields=[
                "id", "fullName", "email", "title", "resumeSlug", "type", "jobName", "status", "createAt"
            ])
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return var_res.Response(serializer.data)

    @action(methods=["get"], detail=False,
            url_path="export", url_name="job-posts-activity-export")
    def export_job_posts_activity(self, request):
        user = request.user

        queryset = self.filter_queryset(self.get_queryset().filter(job_post__company=user.company)
                                        .order_by('-id', 'create_at'))
        serializer = EmployerJobPostActivityExportSerializer(queryset, many=True, fields=[
            "title", "fullName", "email", "phone",
            "gender", "birthday", "address",
            "jobName",
            "createAt", "statusApply"
        ])
        result_data = utils.convert_data_with_en_key_to_vn_kew(serializer.data,
                                                               table_export.JOB_POST_ACTIVITY_FIELD)

        return Response(data=result_data)

    @action(methods=["put"], detail=True,
            url_path="application-status", url_name="application-status")
    def change_application_status(self, request, pk):
        data = request.data

        if data.get("status", None):
            stt = data["status"]
            job_post_activity = self.get_object()
            job_post_activity.status = stt
            job_post_activity.save()

            # send notification
            notification_title = job_post_activity.job_post.company.company_name
            notification_content = f'Hồ sơ ứng tuyển của bạn vào vị trí "{job_post_activity.job_post.job_name}" được cập nhật trạng thái sang "{[x for x in var_sys.APPLICATION_STATUS if x[0] == stt][0][1]}"'
            company_img = job_post_activity.job_post.company.company_image_url
            helper.add_apply_status_notifications(
                notification_title,
                notification_content,
                company_img,
                job_post_activity.user_id
            )
            return var_res.Response(status=status.HTTP_200_OK)
        return var_res.Response(status=status.HTTP_400_BAD_REQUEST)


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
                "id", "jobName", "salary", "frequency",
                "isActive", "career", "city"
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


class JobSeekerStatisticViewSet(viewsets.ViewSet):
    permission_classes = [perms_custom.IsJobSeekerUser]

    # thong ke tong quan
    def general_statistics(self, request):
        user = request.user
        total_apply = JobPostActivity.objects.filter(user=user).count()
        total_save = SavedJobPost.objects.filter(user=user).count()
        total_view = ResumeViewed.objects.filter(resume__user=user).aggregate(Sum('views'))
        total_follow = CompanyFollowed.objects.filter(user=user).count()

        return var_res.response_data(data={
            "totalApply": total_apply,
            "totalSave": total_save,
            "totalView": total_view.get('views__sum', 0) if total_view.get('views__sum') else 0,
            "totalFollow": total_follow
        })

    # dem so nha tuyen dung da xem ho so
    def total_view(self, request):
        user = request.user
        total_view = ResumeViewed.objects.filter(resume__user=user).aggregate(Sum('views'))

        return var_res.response_data(data={
            "totalView": total_view.get('views__sum', 0) if total_view.get('views__sum') else 0,
        })

    # thong ke hoat dong
    def activity_statistics(self, request):
        user = request.user

        now = datetime.datetime.now()
        last_year_today = now.replace(year=now.year - 1)
        first_day_of_month = last_year_today.replace(day=1).date()

        last_day = calendar.monthrange(now.year, now.month)[1]
        last_day_of_month = datetime.datetime(now.year, now.month,
                                              last_day).date()

        queryset1 = JobPostActivity.objects \
            .filter(user=user, create_at__date__range=[first_day_of_month, last_day_of_month]) \
            .order_by('create_at') \
            .annotate(year=ExtractYear('create_at'),
                      month=ExtractMonth('create_at')) \
            .values('year', 'month') \
            .annotate(count=Count('id')) \
            .order_by('year', 'month')

        queryset2 = SavedJobPost.objects \
            .filter(user=user, create_at__date__range=[first_day_of_month, last_day_of_month]) \
            .order_by('create_at') \
            .annotate(year=ExtractYear('create_at'),
                      month=ExtractMonth('create_at')) \
            .values('year', 'month') \
            .annotate(count=Count('id')) \
            .order_by('year', 'month')

        queryset3 = CompanyFollowed.objects \
            .filter(user=user, create_at__date__range=[first_day_of_month, last_day_of_month]) \
            .order_by('create_at') \
            .annotate(year=ExtractYear('create_at'),
                      month=ExtractMonth('create_at')) \
            .values('year', 'month') \
            .annotate(count=Count('id')) \
            .order_by('year', 'month')

        labels = []
        data1 = []
        data2 = []
        data3 = []
        title1 = "Việc đã ứng tuyển"
        title2 = "Việc đã lưu"
        title3 = "Công ty đang theo dõi"
        date_range = pd.date_range(start=first_day_of_month, end=last_day_of_month, freq='M')
        for date in date_range:
            m = date.month
            y = date.year
            items1 = [x for x in queryset1 if x['year'] == y and x['month'] == m]
            if len(items1) > 0:
                data1.append(items1[0]['count'])
            else:
                data1.append(0)

            items2 = [x for x in queryset2 if x['year'] == y and x['month'] == m]
            if len(items2) > 0:
                data2.append(items2[0]['count'])
            else:
                data2.append(0)

            items3 = [x for x in queryset3 if x['year'] == y and x['month'] == m]
            if len(items3) > 0:
                data3.append(items3[0]['count'])
            else:
                data3.append(0)

            labels.append(f'T{m}-{y}')

        return var_res.response_data(data={
            "title1": title1,
            "title2": title2,
            "title3": title3,
            "labels": labels,
            "data1": data1,
            "data2": data2,
            "data3": data3
        })


class EmployerStatisticViewSet(viewsets.ViewSet):
    permission_classes = [perms_custom.IsEmployerUser]

    # thong ke tong quan
    def general_statistics(self, request):
        user = request.user

        total_job_post = JobPost.objects.filter(company=user.company).count()
        total_job_posting_pending_approval = JobPost.objects.filter(company=user.company, is_verify=False).count()
        total_job_post_expired = JobPost.objects \
            .filter(company=user.company, deadline__gte=datetime.datetime.now().date()).count()
        total_apply = JobPostActivity.objects.filter(job_post__company=user.company).count()

        return var_res.response_data(data={
            "totalJobPost": total_job_post,
            "totalJobPostingPendingApproval": total_job_posting_pending_approval,
            "totalJobPostExpired": total_job_post_expired,
            "totalApply": total_apply
        })

    # bieu do tuyen dung
    def recruitment_statistics(self, request):
        data = request.data
        serializer = StatisticsSerializer(data=data)
        if not serializer.is_valid():
            return var_res.response_data(status=status.HTTP_400_BAD_REQUEST,
                                         data=None,
                                         errors=serializer.errors)
        start_date_str = serializer.data.get("startDate")
        end_date_str = serializer.data.get("endDate")

        user = request.user
        queryset = JobPostActivity.objects.filter(job_post__company=user.company) \
            .values(stt=F('status')) \
            .filter(
            Q(create_at__isnull=True) |
            Q(create_at__date__range=[start_date_str, end_date_str])) \
            .annotate(countJobPostActivity=Count('id')) \
            .order_by('-stt')

        data_results = []
        for application_stt in var_sys.APPLICATION_STATUS:
            items = [x["countJobPostActivity"] for x in queryset if x.get("stt") == application_stt[0]]
            if len(items) > 0:
                data_results.append({
                    "label": application_stt[1],
                    "data": items
                })
            else:
                data_results.append({
                    "label": application_stt[1],
                    "data": [0]
                })

        return var_res.response_data(data=data_results)

    # bieu do ung vien
    def candidate_statistics(self, request):
        user = request.user
        data = request.data

        serializer = StatisticsSerializer(data=data)
        if not serializer.is_valid():
            return var_res.response_data(status=status.HTTP_400_BAD_REQUEST,
                                         data=None,
                                         errors=serializer.errors)
        start_date_str = serializer.data.get("startDate")
        end_date_str = serializer.data.get("endDate")
        start_date1 = pd.to_datetime(start_date_str)
        end_date1 = pd.to_datetime(end_date_str)
        start_date2 = start_date1 - timedelta(days=365)
        end_date2 = end_date1 - timedelta(days=365)

        queryset1 = JobPostActivity.objects.filter(job_post__company=user.company,
                                                   create_at__date__range=[start_date1, end_date1]) \
            .annotate(date=TruncDate('create_at')).values('date').annotate(count=Count('id')).order_by('date')
        queryset2 = JobPostActivity.objects.filter(job_post__company=user.company,
                                                   create_at__date__range=[start_date2, end_date2]) \
            .annotate(date=TruncDate('create_at')).values('date').annotate(count=Count('id')).order_by('date')

        title1 = end_date1.year
        title2 = end_date2.year
        labels = []
        data1 = []
        data2 = []
        date_range = pd.date_range(start=start_date1, end=end_date1, freq='D')
        for date in date_range:
            d1 = 0
            d2 = 0
            label = date.strftime("%d/%m")
            items1 = [x for x in queryset1 if x.get("date") == date.date()]
            if len(items1) > 0:
                d1 = items1[0].get("count", 0)
            items2 = [x for x in queryset2 if x.get("date") == date.date()]
            if len(items2) > 0:
                d1 = items2[0].get("count", 0)

            data1.append(d1)
            data2.append(d2)
            labels.append(label)

        return var_res.response_data(data={
            "title1": title1,
            "title2": title2,
            "labels": labels,
            "data1": data1,
            "data2": data2
        })

    # bieu do tuyen dung va ung vien
    def application_statistics(self, request):
        user = request.user
        data = request.data

        serializer = StatisticsSerializer(data=data)
        if not serializer.is_valid():
            return var_res.response_data(status=status.HTTP_400_BAD_REQUEST,
                                         data=None,
                                         errors=serializer.errors)
        start_date_str = serializer.data.get("startDate")
        end_date_str = serializer.data.get("endDate")
        start_date = pd.to_datetime(start_date_str)
        end_date = pd.to_datetime(end_date_str)

        job_post_data = JobPost.objects.filter(company=user.company).values_list("create_at", flat=True)
        job_post_activity_data = JobPostActivity.objects.filter(job_post__company=user.company) \
            .filter(create_at__date__range=[start_date, end_date]).values_list("create_at", flat=True)

        labels = []
        data1 = []
        data2 = []
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        for date in date_range:
            total_job_post = len(list(filter(lambda item: item.date() <= date.date(), job_post_data)))
            total_apply = len(list(filter(lambda item: item.date() == date.date(), job_post_activity_data)))
            label = date.strftime("%d/%m")

            data1.append(total_job_post)
            data2.append(total_apply)
            labels.append(label)

        return var_res.response_data(data={
            "title1": "Việc làm",
            "title2": "Ứng tuyển",
            "labels": labels,
            "data1": data1,
            "data2": data2,
        })

    # bieu do tuyen dung theo cap bac
    def recruitment_statistics_by_rank(self, request):
        data = request.data
        serializer = StatisticsSerializer(data=data)
        if not serializer.is_valid():
            return var_res.response_data(status=status.HTTP_400_BAD_REQUEST,
                                         data=None,
                                         errors=serializer.errors)
        start_date_str = serializer.data.get("startDate")
        end_date_str = serializer.data.get("endDate")

        user = request.user
        data = JobPost.objects.filter(company=user.company) \
            .values(academicLevel=F('academic_level')) \
            .filter(
            Q(jobpostactivity__create_at__isnull=True) |
            Q(jobpostactivity__create_at__date__range=[start_date_str, end_date_str])) \
            .annotate(countJobPostActivity=Count('jobpostactivity')) \
            .order_by('academic_level')

        return var_res.response_data(data=data)

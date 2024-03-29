import json
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import redirect

from configs import variable_system as var_sys
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.contrib import admin
from django.urls import path, include
from django.template.response import TemplateResponse
from django.utils import timezone
from django.db.models import Count, F, Q
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
from datetime import timedelta
from authentication.models import (
    User
)
from job.models import (
    JobPost,
    JobPostActivity
)


class CustomAdminSite(admin.AdminSite):
    site_header = 'MYJOB ADMINISTRATION'
    site_title = 'MyJob site admin'
    index_title = 'Job Portal System'

    dashboard_template = "admin/dashboard.html"
    notifications_template = "admin/notifications.html"
    site_url = "/admin/dashboard/"

    def user_chart(self, request):
        # x <= 31 => by day
        # 31 < x <= 366 => by month
        # 366 <= x => by year
        if request.user.is_anonymous or not request.user.is_staff:
            return HttpResponseForbidden()
        data = json.loads(request.body)

        start_date_str = data.get("startDate", None)
        end_date_str = data.get("endDate", None)
        if start_date_str is None or end_date_str is None:
            return HttpResponseBadRequest()
        start_date = pd.to_datetime(start_date_str)
        end_date = pd.to_datetime(end_date_str)

        days = (end_date - start_date).days

        labels = []
        data1 = []
        data2 = []

        queryset1 = User.objects \
            .filter(create_at__date__range=[start_date, end_date], role_name=var_sys.JOB_SEEKER) \
            .order_by('create_at')
        queryset2 = User.objects \
            .filter(create_at__date__range=[start_date, end_date], role_name=var_sys.EMPLOYER) \
            .order_by('create_at')
        if days <= 31:
            freq = "D"
            queryset1 = queryset1.annotate(year=ExtractYear('create_at'),
                                           month=ExtractMonth('create_at'),
                                           day=ExtractDay('create_at')) \
                .values('year', 'month', 'day') \
                .annotate(count=Count('id')) \
                .order_by('year', 'month', 'day')
            queryset2 = queryset2.annotate(year=ExtractYear('create_at'),
                                           month=ExtractMonth('create_at'),
                                           day=ExtractDay('create_at')) \
                .values('year', 'month', 'day') \
                .annotate(count=Count('id')) \
                .order_by('year', 'month', 'day')
        elif days <= 366:
            freq = "M"
            queryset1 = queryset1.annotate(year=ExtractYear('create_at'),
                                           month=ExtractMonth('create_at')) \
                .values('year', 'month') \
                .annotate(count=Count('id')) \
                .order_by('year', 'month')
            queryset2 = queryset2.annotate(year=ExtractYear('create_at'),
                                           month=ExtractMonth('create_at')) \
                .values('year', 'month') \
                .annotate(count=Count('id')) \
                .order_by('year', 'month')
        else:
            freq = "Y"
            queryset1 = queryset1.annotate(year=ExtractYear('create_at')) \
                .values('year') \
                .annotate(count=Count('id')) \
                .order_by('year')
            queryset2 = queryset2.annotate(year=ExtractYear('create_at')) \
                .values('year') \
                .annotate(count=Count('id')) \
                .order_by('year')

        date_range = pd.date_range(start=start_date, end=end_date, freq=freq)
        for date in date_range:
            d = date.day
            m = date.month
            y = date.year

            if days <= 31:
                label = date.strftime("%d/%m")
                items1 = [x for x in queryset1 if x['year'] == y and x['month'] == m and x['day'] == d]
                if len(items1) > 0:
                    data1.append(items1[0]['count'])
                else:
                    data1.append(0)
                items2 = [x for x in queryset2 if x['year'] == y and x['month'] == m and x['day'] == d]
                if len(items2) > 0:
                    data2.append(items2[0]['count'])
                else:
                    data2.append(0)
            elif days <= 366:
                label = date.strftime("%m/%Y")
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
            else:
                label = date.strftime("%Y")
                items1 = [x for x in queryset1 if x['year'] == y]
                if len(items1) > 0:
                    data1.append(items1[0]['count'])
                else:
                    data1.append(0)
                items2 = [x for x in queryset2 if x['year'] == y]
                if len(items2) > 0:
                    data2.append(items2[0]['count'])
                else:
                    data2.append(0)

            labels.append(label)

        return JsonResponse({
            "labels": labels,
            "data1": data1,
            "data2": data2,
            "title1": "Job seeker",
            "title2": "Employer",
            "color1": "#F8BD7A",
            "color2": "501FC4"
        })

    def job_post_chart(self, request):
        # x <= 31 => by day
        # 31 < x <= 366 => by month
        # 366 <= x => by year
        if request.user.is_anonymous or not request.user.is_staff:
            return HttpResponseForbidden()
        data = json.loads(request.body)

        start_date_str = data.get("startDate", None)
        end_date_str = data.get("endDate", None)
        if start_date_str is None or end_date_str is None:
            return HttpResponseBadRequest()
        start_date = pd.to_datetime(start_date_str)
        end_date = pd.to_datetime(end_date_str)

        days = (end_date - start_date).days

        labels = []
        data1 = []
        data2 = []
        data3 = []

        queryset1 = JobPost.objects \
            .filter(create_at__date__range=[start_date, end_date], status=var_sys.JOB_POST_STATUS[0][0]) \
            .order_by('create_at')
        queryset2 = JobPost.objects \
            .filter(create_at__date__range=[start_date, end_date], status=var_sys.JOB_POST_STATUS[1][0]) \
            .order_by('create_at')
        queryset3 = JobPost.objects \
            .filter(create_at__date__range=[start_date, end_date], status=var_sys.JOB_POST_STATUS[2][0]) \
            .order_by('create_at')
        if days <= 31:
            freq = "D"
            queryset1 = queryset1.annotate(year=ExtractYear('create_at'),
                                           month=ExtractMonth('create_at'),
                                           day=ExtractDay('create_at')) \
                .values('year', 'month', 'day') \
                .annotate(count=Count('id')) \
                .order_by('year', 'month', 'day')
            queryset2 = queryset2.annotate(year=ExtractYear('create_at'),
                                           month=ExtractMonth('create_at'),
                                           day=ExtractDay('create_at')) \
                .values('year', 'month', 'day') \
                .annotate(count=Count('id')) \
                .order_by('year', 'month', 'day')
            queryset3 = queryset3.annotate(year=ExtractYear('create_at'),
                                           month=ExtractMonth('create_at'),
                                           day=ExtractDay('create_at')) \
                .values('year', 'month', 'day') \
                .annotate(count=Count('id')) \
                .order_by('year', 'month', 'day')
        elif days <= 366:
            freq = "M"
            queryset1 = queryset1.annotate(year=ExtractYear('create_at'),
                                           month=ExtractMonth('create_at')) \
                .values('year', 'month') \
                .annotate(count=Count('id')) \
                .order_by('year', 'month')
            queryset2 = queryset2.annotate(year=ExtractYear('create_at'),
                                           month=ExtractMonth('create_at')) \
                .values('year', 'month') \
                .annotate(count=Count('id')) \
                .order_by('year', 'month')
            queryset3 = queryset3.annotate(year=ExtractYear('create_at'),
                                           month=ExtractMonth('create_at')) \
                .values('year', 'month') \
                .annotate(count=Count('id')) \
                .order_by('year', 'month')
        else:
            freq = "Y"
            queryset1 = queryset1.annotate(year=ExtractYear('create_at')) \
                .values('year') \
                .annotate(count=Count('id')) \
                .order_by('year')
            queryset2 = queryset2.annotate(year=ExtractYear('create_at')) \
                .values('year') \
                .annotate(count=Count('id')) \
                .order_by('year')
            queryset3 = queryset3.annotate(year=ExtractYear('create_at')) \
                .values('year') \
                .annotate(count=Count('id')) \
                .order_by('year')

        date_range = pd.date_range(start=start_date, end=end_date, freq=freq)
        for date in date_range:
            d = date.day
            m = date.month
            y = date.year

            if days <= 31:
                label = date.strftime("%d/%m")
                items1 = [x for x in queryset1 if x['year'] == y and x['month'] == m and x['day'] == d]
                if len(items1) > 0:
                    data1.append(items1[0]['count'])
                else:
                    data1.append(0)
                items2 = [x for x in queryset2 if x['year'] == y and x['month'] == m and x['day'] == d]
                if len(items2) > 0:
                    data2.append(items2[0]['count'])
                else:
                    data2.append(0)
                items3 = [x for x in queryset3 if x['year'] == y and x['month'] == m and x['day'] == d]
                if len(items3) > 0:
                    data3.append(items3[0]['count'])
                else:
                    data3.append(0)
            elif days <= 366:
                label = date.strftime("%m/%Y")
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
            else:
                label = date.strftime("%Y")
                items1 = [x for x in queryset1 if x['year'] == y]
                if len(items1) > 0:
                    data1.append(items1[0]['count'])
                else:
                    data1.append(0)
                items2 = [x for x in queryset2 if x['year'] == y]
                if len(items2) > 0:
                    data2.append(items2[0]['count'])
                else:
                    data2.append(0)
                items3 = [x for x in queryset3 if x['year'] == y]
                if len(items3) > 0:
                    data3.append(items3[0]['count'])
                else:
                    data3.append(0)

            labels.append(label)

        return JsonResponse({
            "labels": labels,
            "data1": data1,
            "data2": data2,
            "data3": data3,
            "title1": "Chờ duyệt",
            "title2": "Đã duyệt",
            "title3": "Không duyệt",
            "color1": "#F8BD7A",
            "color2": "#20C41F",
            "color3": "#ff3d00"
        })

    def career_chart(self, request):
        data = json.loads(request.body)

        start_date_str = data.get("startDate", None)
        end_date_str = data.get("endDate", None)
        if start_date_str is None or end_date_str is None:
            return HttpResponseBadRequest()
        start_date = pd.to_datetime(start_date_str)
        end_date = pd.to_datetime(end_date_str)

        labels = []
        data = []

        queryset = JobPost.objects.filter(
            Q(jobpostactivity__create_at__isnull=True) | Q(create_at__date__range=[start_date, end_date])).values(
            'career').annotate(
            total=Count('id')).values('career__name', 'total', ).order_by('-total')[:5]

        return JsonResponse({
            "labels": [x["career__name"] for x in queryset],
            "backgroundColors": ["#32316A", "#000000", "#4a148c", "#2CA58D", "#ffb74d"],
            "data": [x["total"] for x in queryset],
        })

    def application_chart(self, request):
        if request.user.is_anonymous or not request.user.is_staff:
            return HttpResponseForbidden()
        data = json.loads(request.body)

        start_date_str = data.get("startDate", None)
        end_date_str = data.get("endDate", None)
        if start_date_str is None or end_date_str is None:
            return HttpResponseBadRequest()
        start_date = pd.to_datetime(start_date_str)
        end_date = pd.to_datetime(end_date_str)

        labels = []
        data = []

        queryset = JobPostActivity.objects \
            .values(statusApply=F('status')) \
            .filter(create_at__date__range=[start_date, end_date]) \
            .annotate(countStatus=Count('id')) \
            .order_by('status')

        for sys_apply_status in var_sys.APPLICATION_STATUS:
            stt_id = sys_apply_status[0]
            name = sys_apply_status[1]

            items = [x for x in queryset if x["statusApply"] == stt_id]
            if len(items) > 0:
                data.append(items[0]['countStatus'])
                labels.append(name)
            else:
                data.append(0)
                labels.append(name)

        return JsonResponse({
            "labels": labels,
            "data": data,
            "backgroundColors": ["#FFA533", "#FFBD33", "#DBFF33", "#75FF33", "#33FF57", "#FF5733"],
        })

    def dashboard(self, request, extra_context=None):
        if request.user.is_anonymous or not request.user.is_staff:
            return redirect('/admin/login/?next=/admin/notifications/')

        now = timezone.now()
        last_month = now.replace(day=1) - timedelta(days=1)

        # so luong ung vien dang ky
        job_seeker_queryset = User.objects.filter(role_name=var_sys.JOB_SEEKER)
        total_job_seeker = job_seeker_queryset.count()
        last_month_total_job_seeker = job_seeker_queryset.filter(create_at__lte=last_month).count()

        # so luong nha tuyen dung dang ky
        employer_queryset = User.objects.filter(role_name=var_sys.EMPLOYER)
        total_employer = employer_queryset.count()
        last_month_total_employer = employer_queryset.filter(create_at__lte=last_month).count()

        # so luong viec lam
        job_post_queryset = JobPost.objects.filter()
        total_job_post = job_post_queryset.count()
        last_month_total_job_post = job_post_queryset.filter(create_at__lte=last_month).count()

        # so luong ung tuyen
        job_post_activity_queryset = JobPostActivity.objects.filter()
        total_job_post_activity = job_post_activity_queryset.count()
        last_month_total_job_post_activity = job_post_activity_queryset.filter(create_at__lte=last_month).count()

        app_list = self.get_app_list(request)
        each_context_custom = self.each_context(request)
        each_context_custom.update({
            "index_title": "Dashboard",
            'user': request.user,
            'new_candidate': {
                'total': total_job_seeker,
                'current_month_total': total_job_seeker - last_month_total_job_seeker
            },
            'new_employer': {
                'total': total_employer,
                'current_month_total': total_employer - last_month_total_employer
            },
            'job_post': {
                'total': total_job_post,
                'current_month_total': total_job_post - last_month_total_job_post
            },
            'job_post_activity': {
                'total': total_job_post_activity,
                'current_month_total': total_job_post_activity - last_month_total_job_post_activity
            }
        })
        context = {
            **each_context_custom,
            "title": "Dashboard",
            "subtitle": None,
            "app_list": app_list,
            **(extra_context or {}),
        }

        request.current_app = self.name
        return TemplateResponse(
            request, self.dashboard_template or "admin/dashboard.html", context
        )

    def notifications(self, request, extra_context=None):
        if request.user.is_anonymous or not request.user.is_staff:
            return redirect('/admin/login/?next=/admin/notifications/')

        app_list = self.get_app_list(request)

        each_context_custom = self.each_context(request)
        each_context_custom.update({
            "index_title": "Notifications",
        })
        context = {
            **each_context_custom,
            "title": "Notifications",
            "subtitle": None,
            "app_list": app_list,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(
            request, self.notifications_template or "admin/notifications.html", context
        )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("dashboard/", self.dashboard, name="dashboard"),
            path("notifications/", self.notifications, name="notifications"),
            path("api/", include([
                path("user-chart/", self.user_chart, name="dashboard_user_chart"),
                path("job-post-chart/", self.job_post_chart, name="dashboard_job_post_chart"),
                path("career-chart/", self.career_chart, name="dashboard_career_chart"),
                path("application-chart/", self.application_chart, name="dashboard_application_chart")
            ]))
        ]
        return my_urls + urls

    def get_app_list(self, request, app_label=None):
        app_list = [
            {
                "name": "General",
                "app_label": "general_app",
                "models": [
                    {
                        "name": "Dashboard",
                        "object_name": "dashboard",
                        "admin_url": "/admin/dashboard/",
                        "view_only": True,
                    },
                    {
                        "name": "Notifications",
                        "object_name": "notifications",
                        "admin_url": "/admin/notifications/",
                        "view_only": True,
                    }
                ],
            }
        ]
        return app_list + super().get_app_list(request)


custom_admin_site = CustomAdminSite(name='custom_admin')

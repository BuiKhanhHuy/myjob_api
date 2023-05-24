import json
import pandas as pd
import pytz
from django.views.decorators.csrf import csrf_exempt
from configs import variable_system as var_sys
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from django.utils import timezone
from django.db.models import Count, F, Q, Sum
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
from datetime import timedelta
from authentication.models import (
    User
)
from job.models import (
    JobPost,
    JobPostActivity
)


def index(request):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect('/admin/login/?next=/admin/')

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

    context = {'user': request.user,
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
               }
    return render(request, 'pages/dashboard.html', context)


def notifications(request):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect('/admin/login/?next=/admin/notifications/')
    return render(request, 'pages/tables.html')


def billing(request):
    return HttpResponseNotFound()


def profile(request):
    return HttpResponseNotFound()


def tables(request):
    return HttpResponseNotFound()


def rtl(request):
    return HttpResponseNotFound()


def vr(request):
    return HttpResponseNotFound()


@csrf_exempt
def user_chart(request):
    # x <= 31 => by day
    # 31 < x <= 366 => by month
    # 366 <= x => by year
    if request.user.is_anonymous or not request.user.is_superuser:
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
        "color1": "#2196f3",
        "color2": "#dd2c00"
    })


@csrf_exempt
def job_post_chart(request):
    # x <= 31 => by day
    # 31 < x <= 366 => by month
    # 366 <= x => by year
    if request.user.is_anonymous or not request.user.is_superuser:
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

    queryset1 = JobPost.objects \
        .filter(create_at__date__range=[start_date, end_date], is_verify=True) \
        .order_by('create_at')
    queryset2 = JobPost.objects \
        .filter(create_at__date__range=[start_date, end_date], is_verify=False) \
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
        "title1": "Đã duyệt",
        "title2": "Chưa duyệt",
        "color1": "#64dd17",
        "color2": "#dd2c00"
    })


@csrf_exempt
def career_chart(request):
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
        total=Count('id')).values('career__name', 'total',).order_by('-total')[:5]

    return JsonResponse({
        "labels":  [x["career__name"] for x in queryset],
        "backgroundColors": ["#00c853", "#1de9b6", "#00e5ff", "#cddc39", "#ffb74d"],
        "data": [x["total"] for x in queryset],
    })


@csrf_exempt
def application_chart(request):
    if request.user.is_anonymous or not request.user.is_superuser:
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
        "backgroundColors": ["#fb8c00", "#eeff41", "#00e5ff", "#1de9b6", "#64dd17", "#ff3d00"],
    })

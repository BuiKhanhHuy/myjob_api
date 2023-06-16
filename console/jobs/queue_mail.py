from configs import variable_system as var_sys
from django.conf import settings
from datetime import datetime
from helpers import utils, helper
from celery import shared_task
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from job.models import (
    JobPost,
    JobPostNotification
)


@shared_task
def send_email_verify_email_task(to, data=None, cc=None, bcc=None):
    if data is None:
        data = {}
    subject = "Xác thực email"

    data["my_email"] = var_sys.COMPANY_INFO["EMAIL"]
    data["my_phone"] = var_sys.COMPANY_INFO["PHONE"]
    data["my_logo_link"] = var_sys.COMPANY_INFO["DARK_LOGO_LINK"]
    data["my_address"] = var_sys.COMPANY_INFO["ADDRESS"]
    data["now"] = datetime.now().date().strftime(var_sys.DATE_TIME_FORMAT["dmY"])

    email_html = render_to_string('verify-email.html', data)
    text_content = strip_tags(email_html)
    sent = utils.send_mail(subject, text_content, email_html, to=to)

    if sent:
        return 'Email verify sent successfully.'
    else:
        return 'Email verify sent failed!'


@shared_task
def send_email_reset_password_for_web_task(to, reset_password_url, cc=None, bcc=None):
    subject = "Đặt lại mật khẩu"

    data = {
        "my_email": var_sys.COMPANY_INFO["EMAIL"],
        "my_phone": var_sys.COMPANY_INFO["PHONE"],
        "my_logo_link": var_sys.COMPANY_INFO["DARK_LOGO_LINK"],
        "my_address": var_sys.COMPANY_INFO["ADDRESS"],
        "now": datetime.now().date().strftime(var_sys.DATE_TIME_FORMAT["dmY"]),
        "reset_password_url": reset_password_url
    }

    email_html = render_to_string('forgot-password.html', data)
    text_content = strip_tags(email_html)
    sent = utils.send_mail(subject, text_content, email_html, to=to, cc=cc, bcc=bcc)

    if sent:
        return 'Email reset password sent successfully.'
    else:
        return 'Email reset password sent failed!'


@shared_task
def send_email_reset_password_for_app_task(to, full_name, code, cc=None, bcc=None):
    subject = f"{code} là mã xác nhận quên mật khẩu tài khoản MyJob của bạn"

    data = {
        "my_email": var_sys.COMPANY_INFO["EMAIL"],
        "my_phone": var_sys.COMPANY_INFO["PHONE"],
        "my_logo_link": var_sys.COMPANY_INFO["DARK_LOGO_LINK"],
        "my_address": var_sys.COMPANY_INFO["ADDRESS"],
        "now": datetime.now().date().strftime(var_sys.DATE_TIME_FORMAT["dmY"]),
        "full_name": full_name,
        "code": code
    }

    email_html = render_to_string('app-forgot-password.html', data)
    text_content = strip_tags(email_html)
    sent = utils.send_mail(subject, text_content, email_html, to=to, cc=cc, bcc=bcc)

    if sent:
        return 'Email reset password for app sent successfully.'
    else:
        return 'Email reset password for app sent failed!'


@shared_task
def send_email_reply_job_seeker_task(to, subject, data=None, cc=None, bcc=None):
    if data is None:
        data = {}
    data["my_email"] = var_sys.COMPANY_INFO["EMAIL"]
    data["my_phone"] = var_sys.COMPANY_INFO["PHONE"]
    data["my_logo_link"] = var_sys.COMPANY_INFO["DARK_LOGO_LINK"]
    data["my_address"] = var_sys.COMPANY_INFO["ADDRESS"]
    data["now"] = datetime.now().date().strftime(var_sys.DATE_TIME_FORMAT["dmY"])

    email_html = render_to_string('send-email-reply-to-job-seeker.html', data)
    text_content = strip_tags(email_html)
    sent = utils.send_mail(subject, text_content, email_html, to=to, cc=cc, bcc=bcc)

    if sent:
        return 'Email reply to job seeker sent successfully.'
    else:
        return 'Email reply to job seeker sent failed!'


@shared_task
def send_email_confirm_application(to, subject, data=None, cc=None, bcc=None):
    try:
        if data is None:
            data = {}
        data["my_email"] = var_sys.COMPANY_INFO["EMAIL"]
        data["my_phone"] = var_sys.COMPANY_INFO["PHONE"]
        data["my_logo_link"] = var_sys.COMPANY_INFO["DARK_LOGO_LINK"]
        data["my_address"] = var_sys.COMPANY_INFO["ADDRESS"]
        data["now"] = datetime.now().date().strftime(var_sys.DATE_TIME_FORMAT["dmY"])

        email_html = render_to_string('application-confirm.html', data)
        text_content = strip_tags(email_html)
        sent = utils.send_mail(subject, text_content, email_html, to=to, cc=cc, bcc=bcc)

        if sent:
            return 'Email confirm application sent successfully.'
        else:
            return 'Email confirm application sent failed!'
    except Exception as ex:
        helper.print_log_error("send_email_confirm_application", ex)
        return "Email confirm application sent failed with error!"


@shared_task
def send_email_confirm_application(to, subject, data=None, cc=None, bcc=None):
    try:
        if data is None:
            data = {}
        data["my_email"] = var_sys.COMPANY_INFO["EMAIL"]
        data["my_phone"] = var_sys.COMPANY_INFO["PHONE"]
        data["my_logo_link"] = var_sys.COMPANY_INFO["DARK_LOGO_LINK"]
        data["my_address"] = var_sys.COMPANY_INFO["ADDRESS"]
        data["now"] = datetime.now().date().strftime(var_sys.DATE_TIME_FORMAT["dmY"])

        email_html = render_to_string('application-confirm.html', data)
        text_content = strip_tags(email_html)
        sent = utils.send_mail(subject, text_content, email_html, to=to, cc=cc, bcc=bcc)

        if sent:
            return 'Email confirm application sent successfully.'
        else:
            return 'Email confirm application sent failed!'
    except Exception as ex:
        helper.print_log_error("send_email_confirm_application", ex)
        return "Email confirm application sent failed with error!"


@shared_task
def send_email_for_user(user_id, full_name, to_email, frequency):
    try:
        job_post_list = []
        # lay danh sach cai dat thong bao
        job_post_notifications = JobPostNotification.objects \
            .filter(user_id=user_id, is_active=True, frequency=frequency) \
            .values("job_name", "position", "experience", "salary", "career", "city")

        # huy do chua co thiet lap thong bao
        if job_post_notifications.count() == 0:
            return f'Send job notification email to {to_email} cancel. Due to not setting up job notifications'

        for job_post_notification in job_post_notifications:
            query = JobPost.objects.filter(
                status=var_sys.JOB_POST_STATUS[2][0],
                deadline__gte=datetime.now().date(),
                job_name__icontains=job_post_notification.get("job_name", None),
                career=job_post_notification.get("career", None),
                location__city=job_post_notification.get("city", None),
            )
            if job_post_notification.get("position", None):
                query = query.filter(position=job_post_notification.get("position", None))
            if job_post_notification.get("experience", None):
                query = query.filter(experience=job_post_notification.get("experience", None))
            if job_post_notification.get("salary", None):
                query = query.filter(salary_min__lte=job_post_notification.get("salary", None),
                                     salary_max__gte=job_post_notification.get("salary", None))

            job_posts = query.values("id", "slug", "job_name", "career__name",
                                     "location__city__name", "salary_min",
                                     "salary_max", "company__company_name",
                                     "company__company_image_url",
                                     "company__slug",
                                     "position")[:3]
            job_post_list.extend(job_posts)

        total_result = len(job_post_list)
        if total_result == 0:
            return f"Send job notification email to {to_email} cancel. Can't find any suitable job"

        subject = f'Việc làm {job_post_list[0].get("job_name")} '
        if total_result > 1:
            subject += f"và {total_result - 1} công việc khác "

        subject += "cho bạn"
        app_env = settings.APP_ENVIRONMENT
        domain = settings.DOMAIN_CLIENT[app_env]
        data = {
            "my_address": var_sys.COMPANY_INFO["ADDRESS"],
            "full_name": full_name,
            "description": f"Chúng tôi đã tìm thấy {total_result} công việc phù hợp với yêu cầu của bạn.",
            "job_post_link": f"{domain}viec-lam/",
            "company_link": f"{domain}cong-ty/",
            "job_post_notification_link": f"{domain}ung-vien/viec-lam-cua-toi/?tab=3",
            "job_post_list": job_post_list
        }
        # print("subject: ", subject)
        # print("data: ", data)
        # print("\n")

        email_html = render_to_string('suggested-job-post.html', data)
        text_content = strip_tags(email_html)
        sent = utils.send_mail(subject, text_content, email_html, to=[to_email])

        if sent:
            return f'Send job notification email to {to_email} successfully.'
        else:
            return f'Send job notification email to {to_email} failed.'
    except Exception as ex:
        helper.print_log_error("send_email_for_user", ex)
        return f'Send job notification email to {to_email} has errors.'

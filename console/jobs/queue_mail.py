from configs import variable_system as var_sys
from datetime import datetime
from helpers import utils, helper
from celery import shared_task
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from info.models import Resume
from job.models import JobPost


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

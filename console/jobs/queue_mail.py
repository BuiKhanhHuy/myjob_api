from helpers import utils
from celery import shared_task
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task
def send_email_verify_email_task(to, data=None, cc=None, bcc=None):
    if data is None:
        data = {}
    subject = "Xác thực email"

    email_html = render_to_string('verify-email.html', data)
    text_content = strip_tags(email_html)
    sent = utils.send_mail(subject, text_content, email_html, to=to)

    if sent:
        return 'Email verify sent successfully.'
    else:
        return 'Email verify sent failed!'


@shared_task
def send_email_reset_password_task(to, data=None, cc=None, bcc=None):
    if data is None:
        data = {}
    subject = "Đặt lại mật khẩu"

    email_html = render_to_string('forgot-password.html', data)
    text_content = strip_tags(email_html)
    sent = utils.send_mail(subject, text_content, email_html, to=to)

    if sent:
        return 'Email reset password sent successfully.'
    else:
        return 'Email reset password sent failed!'


@shared_task
def send_email_apply_job_task():
    return "AHIHI"


@shared_task
def send_email_reply_job_seeker_task(subject, recipient, template_name, data=None, cc=None, bcc=None):
    pass

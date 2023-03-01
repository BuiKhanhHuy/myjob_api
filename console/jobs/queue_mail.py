from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_email_task(recipient, subject, message):
    send_mail(
        subject,
        message,
        'joblink.easy@gmail.com',
        [recipient],
        fail_silently=False,
    )

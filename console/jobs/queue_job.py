import math
from configs import variable_system as var_sys
from django.db.models import Count
from celery import shared_task, chord
from authentication.models import User
from . import queue_mail


@shared_task
def send_email_job_post_callback(results):
    # Code to handle results after all tasks have completed
    return "Send all success"


@shared_task
def send_email_job_post_for_job_seeker_task(frequency, max_size=100):
    users = User.objects.filter(is_active=True, is_verify_email=True,
                                role_name=var_sys.JOB_SEEKER, email='khuy220@gmail.com')
    total_user = users.count()

    tasks = []

    for i in range(0, math.ceil(total_user / max_size)):
        start = i * max_size
        n = total_user - (max_size * i)

        if n < max_size:
            end = (start + n)
        else:
            end = (start + max_size)

        batch_users = users[start:end]

        tasks.extend(
            [queue_mail.send_email_for_user.s(user.id, user.full_name, user.email, frequency) for user in batch_users]
        )

    # Schedule tasks in parallel using a chord
    chord(tasks)(send_email_job_post_callback.s())

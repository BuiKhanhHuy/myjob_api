from celery import shared_task


@shared_task
def send_email_job_post_for_job_seeker_task():
    return "AHIHI"


@shared_task
def send_email_resume_for_employer_task(subject, recipient, template_name, data=None, cc=None, bcc=None):
    pass

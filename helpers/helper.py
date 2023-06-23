import time
from datetime import datetime
from django.conf import settings

from configs import variable_system as var_sys
from console.jobs import queue_mail, queue_notification
from authentication.tokens_custom import email_verification_token
from authentication.models import User
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes


def print_log_error(func_name, error, now=datetime.now()):
    print(f">>> ERROR [{now}][{func_name}] >> {error}")


def get_full_client_url(func):
    app_env = settings.APP_ENVIRONMENT

    return settings.DOMAIN_CLIENT[app_env] + func


def check_expiration_time(expiration_time):
    return expiration_time - int(time.time()) > 0


def urlsafe_base64_encode_with_expires(data, expires_in_seconds):
    base64_data = urlsafe_base64_encode(force_bytes(data))

    current_time = int(time.time())
    expiration_time = current_time + expires_in_seconds
    base64_time = urlsafe_base64_encode(force_bytes(expiration_time))

    encoded_data = f"{base64_data}|{base64_time}"

    return encoded_data


def urlsafe_base64_decode_with_encoded_data(encoded_data):
    try:
        encoded_data_split = str(encoded_data).split("|")

        data = force_str(urlsafe_base64_decode(encoded_data_split[0]))
        expiration_time = force_str(urlsafe_base64_decode(encoded_data_split[1]))

        return data, int(expiration_time)
    except:
        return None, None


def send_email_verify_email(request, user, platform):
    role_name = user.role_name
    redirect_login = settings.REDIRECT_LOGIN_CLIENT[role_name]

    # send mail verify email
    encoded_data = urlsafe_base64_encode_with_expires(
        user.pk, settings.MYJOB_AUTH["VERIFY_EMAIL_LINK_EXPIRE_SECONDS"]
    )
    token = email_verification_token.make_token(user=user)
    func = f"api/auth/active-email/{encoded_data}/{token}/?redirectLogin={redirect_login}&platform=WEB"

    protocol = 'https' if request.is_secure() else 'http'
    domain = request.META['HTTP_HOST']

    confirm_email_deeplink = None
    if role_name == var_sys.JOB_SEEKER and platform == "APP":
        confirm_email_deeplink = f"{settings.DOMAIN_CLIENT[settings.APP_ENVIRONMENT]}active/{encoded_data}/{token}/APP"

    data = {
        "confirm_email_url": f'{protocol}://{domain}/{func}',
        "confirm_email_deeplink": confirm_email_deeplink
    }

    # send mail verify
    queue_mail.send_email_verify_email_task.delay(to=[user.email], data=data)


def send_email_reply_to_job_seeker(to, subject, data):
    queue_mail.send_email_reply_job_seeker_task.delay(to=to, subject=subject, data=data)


def add_system_notifications(title, content, user_id_list):
    try:
        type_name = var_sys.NOTIFICATION_TYPE["SYSTEM"]
        queue_notification.add_notification_to_user.delay(title=title, content=content,
                                                          type_name=type_name, user_id_list=user_id_list)
    except Exception as ex:
        print_log_error("add_system_notifications", ex)


def add_employer_viewed_resume_notifications(title, content, company_image, user_id):
    try:
        type_name = var_sys.NOTIFICATION_TYPE["EMPLOYER_VIEWED_RESUME"]
        queue_notification.add_notification_to_user.delay(title=title, content=content,
                                                          type_name=type_name,
                                                          image=company_image,
                                                          user_id_list=[user_id])
    except Exception as ex:
        print_log_error("add_employer_viewed_resume_notifications", ex)


def add_employer_saved_resume_notifications(title, content, company_image, user_id):
    try:
        type_name = var_sys.NOTIFICATION_TYPE["EMPLOYER_SAVED_RESUME"]
        queue_notification.add_notification_to_user.delay(title=title, content=content,
                                                          type_name=type_name,
                                                          image=company_image,
                                                          user_id_list=[user_id])
    except Exception as ex:
        print_log_error("add_employer_saved_resume_notifications", ex)


def add_apply_status_notifications(title, content, image, user_id):
    try:
        type_name = var_sys.NOTIFICATION_TYPE["APPLY_STATUS"]
        queue_notification.add_notification_to_user.delay(title=title, content=content,
                                                          image=image,
                                                          type_name=type_name, user_id_list=[user_id])
    except Exception as ex:
        print_log_error("add_apply_status_notifications", ex)


def add_company_followed_notifications(title, content, avatar, user_id):
    try:
        type_name = var_sys.NOTIFICATION_TYPE["COMPANY_FOLLOWED"]
        queue_notification.add_notification_to_user.delay(title=title, content=content,
                                                          image=avatar,
                                                          type_name=type_name, user_id_list=[user_id])
    except Exception as ex:
        print_log_error("add_company_followed_notifications", ex)


def add_apply_job_notifications(job_post_activity):
    try:
        title = f"Ứng viên {job_post_activity.full_name} - {job_post_activity.email}"
        content = f'Đã ứng tuyển vị trí "{job_post_activity.job_post.job_name}"'
        avatar = job_post_activity.user.avatar_url
        content_of_type = {
            "resume_id": job_post_activity.resume_id,
            "resume_slug": job_post_activity.resume.slug
        }
        user_id = job_post_activity.job_post.user_id
        type_name = var_sys.NOTIFICATION_TYPE["APPLY_JOB"]
        queue_notification.add_notification_to_user.delay(title=title, content=content,
                                                          image=avatar,
                                                          content_of_type=content_of_type,
                                                          type_name=type_name, user_id_list=[user_id])
    except Exception as ex:
        print_log_error("add_apply_job_notifications", ex)


def add_post_verify_required_notifications(company, job_post):
    try:
        job_post_id = job_post.id
        job_post_title = job_post.job_name

        title = company.company_name
        content = f'Request to browse job posting "{job_post_title}"'
        company_image = company.company_image_url

        user_id_list = list(User.objects.filter(is_staff=True).values_list('id', flat=True))

        type_name = var_sys.NOTIFICATION_TYPE["POST_VERIFY_REQUIRED"]
        content_of_type = {
            "job_post_id": job_post_id,
        }
        queue_notification.add_notification_to_user.delay(title=title, content=content,
                                                          content_of_type=content_of_type,
                                                          image=company_image,
                                                          type_name=type_name, user_id_list=user_id_list)
    except Exception as ex:
        print_log_error("add_post_verify_required_notifications", ex)


def add_job_post_verify_notification(job_post):
    try:
        stt_str = [x[1] for x in var_sys.JOB_POST_STATUS if x[0] == job_post.status][0]
        title = "Thông báo hệ thống"
        content = f'Tin tuyển dụng "{job_post.job_name}" đã được chuyển sang trạng thái "{stt_str}"'

        type_name = var_sys.NOTIFICATION_TYPE["POST_VERIFY_RESULT"]
        queue_notification.add_notification_to_user.delay(title=title, content=content,
                                                          type_name=type_name, user_id_list=[job_post.user_id])
    except Exception as ex:
        print_log_error("add_job_post_verify_notification", ex)

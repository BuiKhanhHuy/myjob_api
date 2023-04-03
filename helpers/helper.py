from django.conf import settings
import time
from datetime import datetime
from configs import variable_system as var_sys
from console.jobs import queue_mail
from authentication.tokens_custom import email_verification_token
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


def send_email_verify_email(request, user):
    role_name = user.role_name
    redirect_login = settings.REDIRECT_LOGIN_CLIENT[role_name]

    # send mail verify email
    encoded_data = urlsafe_base64_encode_with_expires(
        user.pk, settings.MYJOB_AUTH["VERIFY_EMAIL_LINK_EXPIRE_SECONDS"]
    )
    token = email_verification_token.make_token(user=user)
    func = f"api/auth/active-email/{encoded_data}/{token}/?redirectLogin={redirect_login}"

    protocol = 'https' if request.is_secure() else 'http'
    domain = request.META['HTTP_HOST']

    data = {
        "confirm_email_url": f'{protocol}://{domain}/{func}'
    }

    # send mail verify
    queue_mail.send_email_verify_email_task.delay(to=[user.email], data=data)


def send_email_reset_password(user):
    app_env = settings.APP_ENVIRONMENT

    encoded_data = urlsafe_base64_encode_with_expires(
        user.pk, settings.MYJOB_AUTH["RESET_PASSWORD_LINK_EXPIRE_SECONDS"]
    )

    domain = settings.DOMAIN_CLIENT[app_env]
    func = f"cap-nhat-mat-khau/{encoded_data}"

    data = {
        "reset_password_url": domain + func
    }

    # send mail reset password
    queue_mail.send_email_reset_password_task.delay(to=[user.email], data=data)

import json
import datetime

import cloudinary.uploader
from django.conf import settings
from django.db import transaction

from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django_otp.oath import TOTP
from configs import variable_system as var_sys
from configs.variable_response import response_data
from helpers import helper
from django.http import HttpResponseRedirect, HttpResponseNotFound
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.exceptions import BadRequest
from drf_social_oauth2.views import TokenView, ConvertTokenView
from oauth2_provider.models import get_access_token_model

from console.jobs import queue_mail
from .tokens_custom import email_verification_token
from .models import User, ForgotPasswordToken
from .serializers import (
    CheckCredsSerializer,
    ForgotPasswordSerializer,
    UpdatePasswordSerializer,
    ResetPasswordSerializer,
    EmployerRegisterSerializer,
    JobSeekerRegisterSerializer,
    UserSerializer,
    AvatarSerializer
)


class CustomTokenView(TokenView):
    def post(self, request, *args, **kwargs):
        mutable_data = request.data.copy()
        role_name_input = mutable_data.get("role_name", None)
        if mutable_data["grant_type"] == "password" and not role_name_input:
            return response_data(status=status.HTTP_400_BAD_REQUEST)

        request._request.POST = request._request.POST.copy()
        for key, value in mutable_data.items():
            request._request.POST[key] = value

        url, headers, body, stt = self.create_token_response(request._request)

        if stt == status.HTTP_200_OK:
            if mutable_data["grant_type"] == "password":
                body_data = json.loads(body)
                access_token = body_data.get("access_token")
                if access_token is not None:
                    token = get_access_token_model().objects.get(token=access_token)
                    role_name = token.user.role_name
                    if not role_name == role_name_input:
                        return response_data(status=status.HTTP_400_BAD_REQUEST)
            return response_data(status=stt, data=json.loads(body))
        if stt == status.HTTP_400_BAD_REQUEST:
            return response_data(status=stt, errors={
                "errorMessage": ["Email hoặc mật khẩu không chính xác."]
            })
        else:
            return response_data(status=stt)


class CustomConvertTokenView(ConvertTokenView):
    def post(self, request, *args, **kwargs):
        try:
            mutable_data = request.data.copy()
            request._request.POST = request._request.POST.copy()
            for key, value in mutable_data.items():
                request._request.POST[key] = value

            url, headers, body, stt = self.create_token_response(request._request)
            return response_data(status=stt, data=json.loads(body))
        except BadRequest as ex:
            str_ex = str(ex)
            return response_data(
                status=status.HTTP_400_BAD_REQUEST,
                errors={"errorMessage": [str_ex]}
            )


@api_view(http_method_names=['post'])
def check_email_exists(request):
    data = request.data
    return response_data(status=status.HTTP_200_OK,
                         data=['ahihi'])


@api_view(http_method_names=["POST"])
def check_creds(request):
    data = request.data
    res_data = {
        "exists": False,
        "email": "",
        "email_verified": False
    }

    check_creds_serializer = CheckCredsSerializer(data=data)
    if not check_creds_serializer.is_valid():
        return response_data(status=status.HTTP_400_BAD_REQUEST, errors=check_creds_serializer.errors)

    serializer_data = check_creds_serializer.data

    email = serializer_data["email"]
    role_name = serializer_data.get("roleName", None)

    user = User.objects.filter(email__iexact=email)
    if role_name is not None:
        user = user.filter(role_name=role_name)

    res_data["email"] = email
    if user.exists():
        user = user.first()
        res_data["exists"] = True
        if user.is_verify_email:
            res_data["email_verified"] = True

    return response_data(data=res_data)


@api_view(http_method_names=["GET"])
def user_active(request, encoded_data, token):
    if "redirectLogin" not in request.GET:
        return HttpResponseNotFound()

    redirect_login = request.GET.get("redirectLogin")
    if redirect_login != settings.REDIRECT_LOGIN_CLIENT[var_sys.JOB_SEEKER] and \
            redirect_login != settings.REDIRECT_LOGIN_CLIENT[var_sys.EMPLOYER]:
        return HttpResponseNotFound()

    try:
        uid, expiration_time = helper.urlsafe_base64_decode_with_encoded_data(encoded_data)
        if uid is None or expiration_time is None:
            return HttpResponseRedirect(
                helper.get_full_client_url(
                    f"{redirect_login}/?errorMessage=Rất tiếc, có vẻ như liên kết xác thực email không hợp lệ."))

        if not helper.check_expiration_time(expiration_time):
            return HttpResponseRedirect(
                helper.get_full_client_url(
                    f"{redirect_login}/?errorMessage=Rất tiếc, có vẻ như liên kết xác thực email đã hết hạn."))

        user = User.objects.get(pk=uid)
    except Exception as ex:
        user = None
        helper.print_log_error("user_active", ex)
    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.is_verify_email = True
        user.save()

        # add notification welcome
        helper.add_system_notifications(
            "Thông báo hệ thống",
            "Chào mừng bạn đến với MyJob! Hãy sẵn sàng khám phá và trải nghiệm hệ thống của chúng tôi để tìm kiếm "
            "công việc mơ ước của bạn.",
            [user.id]
        )
        return HttpResponseRedirect(
            helper.get_full_client_url(f"{redirect_login}/?successMessage=Email đã được xác thực."))
    else:
        return HttpResponseRedirect(
            helper.get_full_client_url(
                f"{redirect_login}/?errorMessage=Rất tiếc, có vẻ như liên kết xác thực email không hợp lệ."))


@api_view(http_method_names=["post"])
def forgot_password(request):
    data = request.data
    forgot_password_serializer = ForgotPasswordSerializer(data=data)
    if not forgot_password_serializer.is_valid():
        return response_data(errors=forgot_password_serializer.errors)

    email = forgot_password_serializer.validated_data.get("email")
    platform = forgot_password_serializer.validated_data.get("platform")

    user = User.objects.filter(email=email).first()
    if user:
        try:
            now = datetime.datetime.now()

            tokens = ForgotPasswordToken.objects \
                .filter(user=user, is_active=True, platform=platform, expired_at__gte=now)
            if tokens.exists():
                token = tokens.first()
                token_created_at = token.create_at
                if (now - token_created_at).total_seconds() < settings.MYJOB_AUTH[
                    "TIME_REQUIRED_FORGOT_PASSWORD"
                ]:
                    return response_data(status=status.HTTP_400_BAD_REQUEST, errors={
                        "errorMessage": [
                            "Bạn vừa gửi yêu cầu gửi email quên mật khẩu vui lòng kiểm tra hộp thư hoặc đợi thêm 2 "
                            "phút để gửi lại email."]
                    })

            with transaction.atomic():
                ForgotPasswordToken.objects.filter(user=user, is_active=True, platform=platform).update(is_active=False)
                expired_at = now + datetime.timedelta(seconds=settings.MYJOB_AUTH["RESET_PASSWORD_EXPIRE_SECONDS"])

                if platform == "WEB":
                    app_env = settings.APP_ENVIRONMENT

                    access_token = urlsafe_base64_encode(force_bytes(user.pk))

                    domain = settings.DOMAIN_CLIENT[app_env]
                    func = f"cap-nhat-mat-khau/{access_token}"
                    reset_password_url = domain + func

                    ForgotPasswordToken.objects.create(user=user, expired_at=expired_at,
                                                       token=access_token, platform=platform)
                    # send mail reset password cho website
                    queue_mail.send_email_reset_password_for_web_task.delay(to=[user.email],
                                                                            reset_password_url=reset_password_url)
                elif platform == "APP":
                    totp = TOTP(settings.SECRET_KEY.encode())
                    code = totp.token()
                    new_token = ForgotPasswordToken.objects.create(user=user, expired_at=expired_at,
                                                                   code=code, platform=platform)
                    # send mail reset password cho app
                    queue_mail.send_email_reset_password_for_app_task.delay(to=[user.email],
                                                                            full_name=user.full_name,
                                                                            code=new_token.code)
        except Exception as ex:
            helper.print_log_error("forgot_password", ex)
            return response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response_data()
    else:
        return response_data(status=status.HTTP_400_BAD_REQUEST, errors={
            "errorMessage": [
                "Email này chưa được sử dụng, bạn hãy đăng ký tham gia MyJob."]
        })


@api_view(http_method_names=["post"])
def reset_password(request):
    data = request.data
    serializer = ResetPasswordSerializer(data=data)
    if not serializer.is_valid():
        return response_data(status=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

    try:
        now = datetime.datetime.now()
        platform = serializer.data.get("platform")
        new_password = serializer.data.get("newPassword")

        if platform == "WEB":
            token = serializer.data.get("token")
            user_id = force_str(urlsafe_base64_decode(token))
            print("user id: ", user_id)

            forgot_password_tokens = ForgotPasswordToken.objects.filter(token=token, user_id=user_id, is_active=True)
            if not forgot_password_tokens.exists():
                return response_data(
                    status=status.HTTP_400_BAD_REQUEST,
                    errors={"errorMessage": ["Rất tiếc, có vẻ như liên kết xác nhận quên mật khẩu không hợp lệ."]}
                )
            else:
                forgot_password_token = forgot_password_tokens.first()
                if forgot_password_token.expired_at < now:
                    return response_data(
                        status=status.HTTP_400_BAD_REQUEST,
                        errors={"errorMessage": ["Rất tiếc, có vẻ như liên kết xác nhận quên mật khẩu đã hết hạn."]}
                    )
                else:
                    with transaction.atomic():
                        user = forgot_password_token.user
                        user.set_password(new_password)
                        user.save()
                        forgot_password_token.is_active = False
                        forgot_password_token.save()
                        role_name = user.role_name

                        redirect_login_url = settings.REDIRECT_LOGIN_CLIENT[role_name]
                        return response_data(data={"redirectLoginUrl": f"/{redirect_login_url}"})
        else:
            code = serializer.data.get("code")
            forgot_password_tokens = ForgotPasswordToken.objects.filter(code=code)
            if not forgot_password_tokens.exists():
                return response_data(
                    status=status.HTTP_400_BAD_REQUEST,
                    errors={"code": ["Mã xác nhận quên mật khẩu không hợp lệ."]}
                )
            else:
                forgot_password_token = forgot_password_tokens.first()
                if forgot_password_token.expired_at < now or not forgot_password_token.is_active:
                    return response_data(
                        status=status.HTTP_400_BAD_REQUEST,
                        errors={"code": ["Mã xác nhận quên mật khẩu đã hết hạn."]}
                    )
                else:
                    with transaction.atomic():
                        user = forgot_password_token.user
                        user.set_password(new_password)
                        user.save()
                        forgot_password_token.is_active = False
                        forgot_password_token.save()

                        return response_data()
    except Exception as ex:
        helper.print_log_error("reset_password", ex)
        return response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(http_method_names=['put'])
@permission_classes(permission_classes=[IsAuthenticated])
def change_password(request):
    try:
        data = request.data
        user = request.user

        reset_pass_serializer = UpdatePasswordSerializer(user, data=data, context={
            'user': request.user
        })
        if not reset_pass_serializer.is_valid():
            return response_data(status=status.HTTP_400_BAD_REQUEST,
                                 errors=reset_pass_serializer.errors)
        reset_pass_serializer.save()
    except Exception as ex:
        helper.print_log_error("change_password", ex)
        return response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return response_data(status=status.HTTP_200_OK)


@api_view(http_method_names=['patch'])
@permission_classes(permission_classes=[IsAuthenticated])
def update_user_account(request):
    try:
        data = request.data
        user = request.user

        user_account_serializer = UserSerializer(user, data=data, partial=True,
                                                 fields=['id', 'fullName'])
        if not user_account_serializer.is_valid():
            return response_data(status=status.HTTP_400_BAD_REQUEST, errors=user_account_serializer.errors)

        user_account_serializer.save()
    except Exception as ex:
        helper.print_log_error("update_user_account", ex)
        return response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        user_info_serializer = UserSerializer(user)
        return response_data(status=status.HTTP_200_OK, data=user_info_serializer.data)


@api_view(http_method_names=['put', 'delete'])
@permission_classes(permission_classes=[IsAuthenticated])
def avatar(request):
    if request.method == "PUT":
        files = request.FILES
        avatar_serializer = AvatarSerializer(request.user, data=files)
        if not avatar_serializer.is_valid():
            return response_data(status=status.HTTP_400_BAD_REQUEST, errors=avatar_serializer.errors)
        try:
            avatar_serializer.save()
        except Exception as ex:
            helper.print_log_error("avatar", ex)
            return response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return response_data(status=status.HTTP_200_OK, data=avatar_serializer.data)
    elif request.method == "DELETE":
        user = request.user
        try:
            if user.avatar_public_id:
                destroy_result = cloudinary.uploader.destroy(user.avatar_public_id)
                if not destroy_result.get("result", "") == "ok":
                    raise Exception("Something went wrong when upload image to cloudinary!")

            user.avatar_url = var_sys.AVATAR_DEFAULT["AVATAR"]
            user.avatar_public_id = None
            user.save()
        except Exception as ex:
            helper.print_log_error("delete_avatar", ex)
            return response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return response_data(status=status.HTTP_204_NO_CONTENT, data={
                "avatarUrl": user.avatar_url
            })
    else:
        return response_data(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(http_method_names=['post'])
def employer_register(request):
    data = request.data
    serializer = EmployerRegisterSerializer(data=data)
    if not serializer.is_valid():
        return response_data(status=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
    try:
        user = serializer.save()
        platform = serializer.validated_data.get("platform")
        if user:
            helper.send_email_verify_email(request, user,
                                           platform=platform)
    except Exception as ex:
        helper.print_log_error("employer_register", ex)
        return response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response_data(status=status.HTTP_201_CREATED)


@api_view(http_method_names=['post'])
def job_seeker_register(request):
    data = request.data
    serializer = JobSeekerRegisterSerializer(data=data)
    if not serializer.is_valid():
        return response_data(status=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

    try:
        user = serializer.save()
        platform = serializer.validated_data.get("platform")
        if user:
            helper.send_email_verify_email(request=request, user=user,
                                           platform=platform)
    except Exception as ex:
        helper.print_log_error("job_seeker_register", ex)
        return response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response_data(status=status.HTTP_201_CREATED)


@api_view(http_method_names=["GET"])
@permission_classes(permission_classes=[IsAuthenticated])
def get_user_info(request):
    user_info = request.user
    user_info_serializer = UserSerializer(user_info)
    return response_data(status=status.HTTP_200_OK, data=user_info_serializer.data)

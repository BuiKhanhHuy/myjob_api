import json
from configs.variable_response import response_data
from console.jobs import queue_mail, thread_mail
from .email_verification_token_generator import email_verification_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from helpers import helper
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_social_oauth2.views import TokenView
from oauth2_provider.models import get_access_token_model

from .models import User
from .serializers import (
    CheckCredsSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    EmployerRegisterSerializer,
    JobSeekerRegisterSerializer,
    UserInfoSerializer,
    UserSerializer
)


class CustomTokenView(TokenView):
    def post(self, request, *args, **kwargs):
        mutable_data = request.data.copy()
        role_name_input = mutable_data.get("role_name", None)
        if mutable_data["grant_type"] == "password" and not role_name_input:
            return response_data(status=status.HTTP_400_BAD_REQUEST, message="Thất bại!")

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
        else:
            return response_data(status=stt)


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


@api_view(http_method_names=["POST"])
def verify_email(request):
    data = request.data

    return response_data(data=request.data)


@api_view(http_method_names=["post"])
def forgot_password(request):
    data = request.data
    forgot_password_serializer = ForgotPasswordSerializer(data=data)
    if not forgot_password_serializer.is_valid():
        pass
    return response_data()


@api_view(http_method_names=['get'])
def reset_password(request):
    data = request.data
    reset_password_serializer = ResetPasswordSerializer(data=data)
    if not reset_password_serializer.is_valid():
        pass
    return response_data(data="DA GUI")


@api_view(http_method_names=['get'])
def change_password(request):
    return response_data()


@api_view(http_method_names=['post'])
def employer_register(request):
    data = request.data
    serializer = EmployerRegisterSerializer(data=data)
    if not serializer.is_valid():
        return response_data(status=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
    try:
        serializer.save()
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
        if user:
            # send mail verify email
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = email_verification_token.make_token(user=user)
            data = {
                "email_subject": "Xác thực email",
                "email_body": f'http://localhost:3000/verify-email/{uidb64}/{token}/',
                "to_email": user.email
            }
            thread_mail.Util.send_email(data=data)
    except Exception as ex:
        helper.print_log_error("job_seeker_register", ex)
        return response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response_data(status=status.HTTP_201_CREATED)


@api_view(http_method_names=["GET"])
@permission_classes(permission_classes=[IsAuthenticated])
def get_user_info(request):
    user_info = request.user
    user_info_serializer = UserInfoSerializer(user_info)
    return response_data(status=status.HTTP_200_OK, data=user_info_serializer.data)


class UserViewSet(viewsets.ViewSet,
                  generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects
    serializer_class = UserSerializer

from configs.variable_response import response_data
from helpers import helper
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..serializers import auth_serializers


@api_view(http_method_names=['post'])
def check_email_exists(request):
    data = request.data
    return response_data(status=status.HTTP_200_OK,
                         data=['ahihi'])


@api_view(http_method_names=['post'])
@permission_classes(permission_classes=[IsAuthenticated])
def reset_password(request):
    pass


@api_view(http_method_names=['post'])
def employer_register(request):
    data = request.data
    serializer = auth_serializers.EmployerRegisterSerializer(data=data)
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
    serializer = auth_serializers.JobSeekerRegisterSerializer(data=data)
    if not serializer.is_valid():
        return response_data(status=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
    try:
        serializer.save()
    except Exception as ex:
        helper.print_log_error("job_seeker_register", ex)
        return response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response_data(status=status.HTTP_201_CREATED)


@api_view(http_method_names=["GET"])
@permission_classes(permission_classes=[IsAuthenticated])
def get_user_info(request):
    user_info = request.user
    user_info_serializer = auth_serializers.UserInfoSerializer(user_info)
    return response_data(status=status.HTTP_200_OK, data=user_info_serializer.data)

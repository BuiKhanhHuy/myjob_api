from datetime import datetime
from configs.variable_response import response_data
from rest_framework.decorators import api_view
from rest_framework import status
from ..serializers import auth_serializers


@api_view(http_method_names=['post'])
def check_email_exists(request):
    data = request.data
    return response_data(status=status.HTTP_200_OK,
                         data=['ahihi'])


@api_view(http_method_names=['post'])
def reset_password(request):
    pass


@api_view(http_method_names=['post'])
def employer_register(request):
    pass


@api_view(http_method_names=['post'])
def job_seeker_register(request):
    data = request.data
    serializer = auth_serializers.JobSeekerRegisterSerializer(data=data)
    if not serializer.is_valid():
        return response_data(status=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
    try:
        serializer.save()
    except Exception as ex:
        print(f">>> ERROR: [{datetime.now()}][job_seeker_register] >> {ex}")
        return response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response_data(status=status.HTTP_201_CREATED)

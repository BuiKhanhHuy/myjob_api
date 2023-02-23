from rest_framework.response import Response
from rest_framework import status as res_status


def data_response(data=None, errors=None):
    if errors is None:
        errors = []
    return {
        'errors': errors,
        'data': data
    }


def response_data(status=res_status.HTTP_200_OK, data=None, errors=None):
    if errors is None:
        errors = []
    return Response(status=status, data=data_response(data, errors))

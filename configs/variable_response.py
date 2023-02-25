from rest_framework.response import Response
from rest_framework import status as res_status


def data_response(message, errors, data):
    return {
        'message': message,
        'errors': errors,
        'data': data
    }


def response_data(status=res_status.HTTP_200_OK, message="Success", errors=None, data=None):
    if errors is None:
        errors = []
    return Response(status=status, data=data_response(message=message, errors=errors, data=data))

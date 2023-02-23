from rest_framework.response import Response


def data_response(data=None, status=1, message="Success"):
    return {
        'status_code': status,
        'message': message,
        'data': data
    }


def response_data(data=None, status=1, message="Success"):
    return Response(data_response(data, status, message))

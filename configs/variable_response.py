"""
MyJob Recruitment System - Part of MyJob Platform

Author: Bui Khanh Huy
Email: khuy220@gmail.com
Copyright (c) 2023 Bui Khanh Huy

License: MIT License
See the LICENSE file in the project root for full license information.
"""

from rest_framework.response import Response
from rest_framework import status as res_status


def data_response(errors, data):
    return {
        'errors': errors,
        'data': data
    }


def response_data(status=res_status.HTTP_200_OK, errors=None, data=None):
    if errors is None:
        errors = {}
    return Response(status=status, data=data_response(errors=errors, data=data))

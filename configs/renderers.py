"""
MyJob Recruitment System - Part of MyJob Platform

Author: Bui Khanh Huy
Email: khuy220@gmail.com
Copyright (c) 2023 Bui Khanh Huy

License: MIT License
See the LICENSE file in the project root for full license information.
"""

from rest_framework.renderers import JSONRenderer
from configs import variable_response


class MyJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = variable_response.data_response({}, None)
        if renderer_context and 'response' in renderer_context:
            response_obj = renderer_context['response']
            if response_obj.status_code >= 400:
                errors = response_obj.data

                if isinstance(errors, dict):
                    response = variable_response.data_response(data=None,
                                                               errors=errors)
                else:
                    response = variable_response.data_response(data=errors,
                                                               errors={})
            elif 200 <= response_obj.status_code < 300:
                response = variable_response.data_response(data=data,
                                                           errors={})
        return super().render(response, accepted_media_type, renderer_context)

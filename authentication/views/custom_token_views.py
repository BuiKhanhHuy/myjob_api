import json
from configs.variable_response import response_data
from rest_framework import status
from drf_social_oauth2.views import TokenView
from oauth2_provider.models import get_access_token_model
from ..models import User


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
                        return response_data(status=status.HTTP_400_BAD_REQUEST, message="Thất bại!")
            return response_data(status=stt, message="Thành công.", data=json.loads(body))
        else:
            return response_data(status=stt, message="Thất bại!")

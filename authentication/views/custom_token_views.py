import json
from rest_framework.response import Response
from rest_framework import status
from drf_social_oauth2.views import TokenView
from oauth2_provider.models import get_access_token_model
from ..models import User


class CustomTokenView(TokenView):
    def post(self, request, *args, **kwargs):
        mutable_data = request.data.copy()
        request._request.POST = request._request.POST.copy()
        email = mutable_data.get("username", "")

        if mutable_data.get("grant_type", "") == "password":
            role = mutable_data.get("role", "")
            if not User.objects.filter(email__iexact=email).exists():
                return Response(status=status.HTTP_408_REQUEST_TIMEOUT)

        for key, value in mutable_data.items():
            request._request.POST[key] = value

        url, headers, body, stt = self.create_token_response(request._request)
        response = Response(data=json.loads(body), status=stt)

        for k, v in headers.items():
            response[k] = v
        return response

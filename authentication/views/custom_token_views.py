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

        for key, value in mutable_data.items():
            request._request.POST[key] = value

        url, headers, body, stt = self.create_token_response(request._request)
        if stt == status.HTTP_200_OK:
            body = json.loads(body)
            access_token = body.get("access_token")
            if access_token is not None:
                token = get_access_token_model().objects.get(token=access_token)
                roles = [r.name for r in token.user.roles.all()]
                body['roles'] = roles
                body = json.dumps(body)

        response = Response(data=json.loads(body), status=stt)

        for k, v in headers.items():
            response[k] = v
        return response

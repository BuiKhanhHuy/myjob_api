from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from oauth2_provider.decorators import protected_resource


@protected_resource()
@api_view(['GET'])
def demo(request):
    return Response(status=status.HTTP_200_OK)

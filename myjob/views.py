from console.jobs import queue_notification
from infobip_channels.sms.channel import SMSChannel
from django.conf import settings
from helpers import helper, utils
from configs import renderers
from configs import variable_response as var_res, variable_system as var_sys, app_setting as app_set
from configs.messages import NOTIFICATION_MESSAGES, ERROR_MESSAGES
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions as perms_sys
from .models import (
    Feedback,
    Banner
)
from .serializers import (
    FeedbackSerializer,
    BannerSerializer
)

class FeedbackViewSet(viewsets.ViewSet,
                      generics.CreateAPIView,
                      generics.ListAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    renderer_classes = [renderers.MyJSONRenderer]

    def get_permissions(self):
        if self.action in ["create"]:
            return [perms_sys.IsAuthenticated()]
        return [perms_sys.AllowAny()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()
                                        .filter(is_active=True).order_by('-rating')[:10])

        serializer = self.get_serializer(queryset, many=True,
                                         fields=['id', 'content', 'rating', 'isActive', 'userDict'])
        return var_res.Response(serializer.data)


@api_view(http_method_names=['post'])
def send_sms_download_app(request):
    data = request.data
    if "phone" not in data:
        return var_res.response_data(status=status.HTTP_400_BAD_REQUEST,
                                     errors={"phone": [ERROR_MESSAGES["PHONE_REQUIRED"]]})
    phone = data.get("phone")
    if not phone:
        return var_res.response_data(status=status.HTTP_400_BAD_REQUEST,
                                     errors={"phone": [ERROR_MESSAGES["INVALID_PHONE"]]})
    try:
        # Initialize the SMS channel with your credentials.
        channel = SMSChannel.from_auth_params(
            {
                "base_url": settings.SMS_BASE_URL,
                "api_key": settings.SMS_API_KEY,
            }
        )
        # Send a message with the desired fields.
        sms_response = channel.send_sms_message(
            {
                "messages": [
                    {
                        "destinations": [{"to": phone}],
                        "text": NOTIFICATION_MESSAGES["DOWNLOAD_APP_MESSAGE"].format(
                            company_name=settings.COMPANY_NAME,
                            link_google_play=var_sys.LINK_GOOGLE_PLAY,
                            link_appstore=var_sys.LINK_APPSTORE
                        )
                    }
                ]
            }
        )
        print(">> SMS SEND: ", sms_response)
    except Exception as ex:
        helper.print_log_error("send_sms_download_app", ex)
        var_res.response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return var_res.response_data()


@api_view(http_method_names=['get'])
def get_web_banner(request):
    banner_queryset = Banner.objects.filter(is_active=True, platform="WEB")
    serializer = BannerSerializer(banner_queryset, many=True, fields=[
        "id", "imageUrl", "buttonText", "description",
        "buttonLink", "isShowButton", "descriptionLocation"
    ])

    return var_res.response_data(data=serializer.data)


@api_view(http_method_names=['get'])
def get_mobile_banner(request):
    banner_type = request.GET.get("type", "HOME")
    if banner_type not in [x[1] for x in var_sys.BANNER_TYPE]:
        return var_res.response_data(status=status.HTTP_400_BAD_REQUEST)
    banner_queryset = Banner.objects.filter(is_active=True, platform="APP")
    serializer = BannerSerializer(banner_queryset, many=True, fields=[
        "id", "imageMobileUrl", "buttonText", "description",
        "buttonLink", "isShowButton", "descriptionLocation"
    ])

    return var_res.response_data(data=serializer.data)


@api_view(http_method_names=['post'])
def send_notification_demo(request):
    # Only allow in development environment
    if settings.APP_ENVIRONMENT == app_set.ENV_PROD:
        return var_res.response_data(status=status.HTTP_403_FORBIDDEN)

    data = request.data

    title = data.get("title", "TEST")
    content = data.get('content', "TEST CONTENT")
    user_list = data.get('userList', [])
    notification_type = data.get("type", "SYSTEM")
    body_content = data.get('bodyContent', {})
    image_link = data.get("imageLink", None)

    queue_notification.add_notification_to_user.delay(
        title=title,
        content=content,
        type_name=notification_type,
        image=image_link,
        content_of_type=body_content,
        user_id_list=user_list
    )
    return var_res.response_data()

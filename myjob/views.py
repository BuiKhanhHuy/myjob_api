from twilio.rest import Client
from django.conf import settings

from helpers import helper
from configs import renderers
from configs import variable_response as var_res, variable_system as var_sys
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions as perms_sys
from .models import (
    Feedback
)
from .serializers import (
    FeedbackSerializer
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
                                     errors={"phone": ["Số điện thoại là bắt buộc."]})
    phone = data.get("phone")
    if not phone:
        return var_res.response_data(status=status.HTTP_400_BAD_REQUEST,
                                     errors={"phone": ["Số điện thoại không hợp lệ."]})
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        message = client.messages.create(from_=settings.TWILIO_PHONE,
                                         body=f'Tin nhắn được gửi từ {settings.COMPANY_NAME}, '
                                              f'Ứng dụng và Website giới thiệu việc làm. '
                                              f'Với {settings.COMPANY_NAME}, '
                                              f'bạn có thể tìm kiếm các công việc phù hợp với nhu cầu '
                                              f'và kinh nghiệm của mình chỉ trong vài phút. '
                                              f'Để tải ứng dụng, bạn có thể truy cập vào link sau: '
                                              f'Android: {var_sys.LINK_GOOGLEPLAY}; iOS: {var_sys.LINK_APPSTORE}. '
                                              f'Hãy cùng trải nghiệm và tìm kiếm công '
                                              f'việc mơ ước của bạn với {settings.COMPANY_NAME} nhé!',
                                         to=f"+84{phone[1:None]}")
        print(message, "=>", f"+84{phone[1:None]}")
    except Exception as ex:
        helper.print_log_error("send_sms_download_app", ex)
        var_res.response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return var_res.response_data()

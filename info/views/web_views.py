from configs import variable_response as var_res
from helpers import helper
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework import permissions as perms_sys
from authentication import permissions as perms_custom
from rest_framework import status

from ..models import (JobSeekerProfile,
                      ExperienceDetail)
from ..serializers.web_serializers import (
    ProfileSerializer,
    ProfileUpdateSerializer,
    ProfileDetailSerializer,
    JobSeekerProfileSerializer,
    ExperienceListSerializer
)


class ProfileView(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ["get_profile_info",
                           "update_profile_info",
                           "get_profile_info_detail"]:
            return [perms_custom.IsJobSeekerUser()]
        return perms_sys.IsAuthenticated()

    def get_profile_info(self, request):
        user = request.user
        try:
            profile = JobSeekerProfile.objects.get(user_id__exact=user.id)
            profile_serializer = ProfileSerializer(profile)
        except Exception as ex:
            helper.print_log_error("get_profile_info", ex)
            return var_res.response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                         message="Lỗi hệ thống!")
        else:
            return var_res.response_data(data=profile_serializer.data)

    def get_profile_info_detail(self, request):
        user = request.user
        try:
            profileDetail = JobSeekerProfile.objects.get(user_id__exact=user.id)
            profile_detail_serializer = ProfileDetailSerializer(profileDetail)
        except Exception as ex:
            helper.print_log_error("get_profile_info_detail", ex)
            return var_res.response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                         message="Lỗi hệ thống!")
        else:
            return var_res.response_data(data=profile_detail_serializer.data)

    def update_profile_info(self, request):
        data = request.data

        try:
            job_seeker_profile = request.user.job_seeker_profile

            serializer = ProfileUpdateSerializer(job_seeker_profile, data=data)
            if not serializer.is_valid():
                return var_res.response_data(status=status.HTTP_400_BAD_REQUEST,
                                             errors=serializer.errors)
            serializer.save()
        except Exception as ex:
            helper.print_log_error("update_profile_info", ex)
            return var_res.response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                         message="Lỗi hệ thống!")
        else:
            return var_res.response_data(data=serializer.data)


class JobSeekerProfileViewSet(viewsets.ViewSet,
                              generics.ListAPIView,
                              generics.RetrieveAPIView):
    queryset = JobSeekerProfile.objects
    serializer_class = JobSeekerProfileSerializer

    def get_permissions(self):
        if self.action in ["get_experiences_detail"]:
            return [perms_custom.IsJobSeekerUser()]
        return perms_sys.IsAuthenticated()

    @action(methods=['get'], detail=True,
            url_path='experiences-detail', url_name='get_current_user')
    def get_experiences_detail(self, request, pk):
        try:
            experiences_detail_queryset = ExperienceDetail.objects.filter(job_seeker_profile_id__exact=pk).all()
            experiences_detail_serializer = ExperienceListSerializer(experiences_detail_queryset, many=True)
        except Exception as ex:
            helper.print_log_error("update_profile_info", ex)
            return var_res.response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                         message="Lỗi hệ thống!")
        else:
            return var_res.response_data(data=experiences_detail_serializer.data)
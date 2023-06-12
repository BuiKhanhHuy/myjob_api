import cloudinary.uploader

from console.jobs import queue_mail
from helpers import utils
from configs import variable_system as var_sys, table_export
from configs import variable_response as var_res, renderers, paginations
from django.db.models import Count, Q, F
from django_filters.rest_framework import DjangoFilterBackend
from helpers import helper
from rest_framework import viewsets, generics, views
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions as perms_sys
from authentication import permissions as perms_custom
from rest_framework import status
from ..models import (
    JobSeekerProfile,
    Resume, ResumeViewed,
    ResumeSaved,
    EducationDetail, ExperienceDetail,
    Certificate, LanguageSkill,
    AdvancedSkill, Company,
    CompanyFollowed, CompanyImage
)
from ..filters import (
    ResumeFilter,
    ResumeSavedFilter,
    CompanyFilter
)
from ..serializers import (
    JobSeekerProfileSerializer,
    ResumeSerializer,
    ResumeDetailSerializer,
    ResumeViewedSerializer,
    ResumeSavedSerializer,
    ResumeSavedExportSerializer,
    CvSerializer,
    EducationSerializer,
    ExperienceSerializer,
    CertificateSerializer,
    LanguageSkillSerializer,
    AdvancedSkillSerializer,
    CompanySerializer,
    CompanyFollowedSerializer,
    LogoCompanySerializer,
    CompanyCoverImageSerializer,
    CompanyImageSerializer,
    SendMailReplyToJobSeekerSerializer
)
from job.models import (
    JobPost
)
from job import serializers as job_serializers


class JobSeekerProfileViewSet(viewsets.ViewSet,
                              generics.ListAPIView,
                              generics.RetrieveAPIView):
    queryset = JobSeekerProfile.objects
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [perms_sys.AllowAny()]

    def get_permissions(self):
        if self.action in ["get_resumes"]:
            return [perms_custom.IsJobSeekerUser()]
        return self.permission_classes

    @action(methods=["get"], detail=True,
            url_path="resumes", url_name="get-resumes")
    def get_resumes(self, request, pk):
        query_params = request.query_params
        resume_type = query_params.get("resumeType", None)

        job_seeker_profile = self.get_object()
        if not job_seeker_profile:
            raise Exception("User doesn't have job_seeker_profile.")

        resumes = job_seeker_profile.resumes
        # get all
        if resume_type is None:
            serializer = ResumeSerializer(resumes, many=True, fields=[
                "id", "slug", "title", "type", "updateAt", "isActive"
            ])
        else:
            # get by type
            if not (resume_type == var_sys.CV_WEBSITE) and not (resume_type == var_sys.CV_UPLOAD):
                return var_res.response_data(status=status.HTTP_400_BAD_REQUEST,
                                             errors={"detail": "resumeType is invalid."})

            resumes = resumes.filter(type=resume_type)
            if resume_type == var_sys.CV_WEBSITE:
                if not resumes.first():
                    return var_res.response_data()
                serializer = ResumeSerializer(resumes.first(),
                                              fields=["id", "slug", "title", "experience", "position",
                                                      "salaryMin", "salaryMax", "updateAt", "user", "isActive"])
            else:
                serializer = ResumeSerializer(resumes, many=True,
                                              fields=["id", "slug", "title", "updateAt",
                                                      "imageUrl", "fileUrl", "isActive"])

        return var_res.response_data(data=serializer.data)


class PrivateResumeViewSet(viewsets.ViewSet,
                           generics.CreateAPIView,
                           generics.UpdateAPIView,
                           generics.DestroyAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ["get_resume_detail_of_job_seeker",
                           "update", "partial_update",
                           "resume_active",
                           "destroy",
                           "get_experiences_detail",
                           "get_educations_detail",
                           "get_certificates_detail",
                           "get_language_skills",
                           "get_advanced_skills"]:
            return [perms_custom.ResumeOwnerPerms()]
        elif self.action in ["create"]:
            return [perms_custom.IsJobSeekerUser()]
        return [perms_sys.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        serializer = ResumeSerializer(data=data, fields=[
            "title", "description", "salaryMin", "salaryMax",
            "position", "experience", "academicLevel", "typeOfWorkplace",
            "jobType", "city", "career", "file"
        ], context={'request': request})
        if not serializer.is_valid():
            return var_res.response_data(status=status.HTTP_400_BAD_REQUEST,
                                         errors=serializer.errors)
        self.perform_create(serializer)
        return var_res.response_data(data=serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial,
                                         fields=[
                                             "id", "slug", "title", "description",
                                             "salaryMin", "salaryMax",
                                             "position", "experience", "academicLevel",
                                             "typeOfWorkplace", "jobType", "isActive",
                                             "city", "career", "updateAt", "file",
                                             "imageUrl", "fileUrl", "user", "city",
                                         ])
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(methods=["get"], detail=True,
            url_path='resume-active', url_name="resume-active", )
    def active_resume(self, request, slug):
        resume = self.get_object()
        if resume.is_active:
            resume.is_active = False
            resume.save()
        else:
            Resume.objects.filter(user=self.request.user) \
                .exclude(slug=resume.slug) \
                .update(is_active=False)
            resume.is_active = True
            resume.save()
        return var_res.response_data()

    @action(methods=["get"], detail=True,
            url_path='resume-owner', url_name="get-resume-detail-of-job-seeker", )
    def get_resume_detail_of_job_seeker(self, request, slug):
        resume_queryset = self.get_object()
        resume_serializer = ResumeSerializer(resume_queryset,
                                             fields=["id", "slug", "title", "salaryMin", "salaryMax",
                                                     "position", "experience", "academicLevel",
                                                     "typeOfWorkplace", "jobType", "description",
                                                     "isActive", "city", "career"])

        return var_res.response_data(data=resume_serializer.data)

    @action(methods=["get"], detail=True,
            url_path='cv', url_name="get-cv", )
    def get_cv(self, request, slug):
        resume_queryset = self.get_object()
        resume_serializer = CvSerializer(resume_queryset,
                                         fields=["id", "slug", "title", "fileUrl"])

        return var_res.response_data(data=resume_serializer.data)

    @get_cv.mapping.put
    def update_cv_file(self, request, slug):
        files = request.FILES
        cv_serializer = CvSerializer(self.get_object(), data=files, fields=["file"])
        if not cv_serializer.is_valid():
            return var_res.response_data(status=status.HTTP_400_BAD_REQUEST,
                                         errors=cv_serializer.errors)
        try:
            cv_serializer.save()
        except Exception as ex:
            helper.print_log_error("update_cv_file", error=ex)
            return var_res.response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return var_res.response_data()

    @action(methods=["get"], detail=True,
            url_path="educations-detail", url_name="get-educations-detail")
    def get_educations_detail(self, request, slug):
        educations_detail_queryset = self.get_object().education_details
        educations_detail_serializer = EducationSerializer(
            educations_detail_queryset,
            many=True)

        return var_res.response_data(data=educations_detail_serializer.data)

    @action(methods=["get"], detail=True,
            url_path="experiences-detail", url_name="get-experiences-detail")
    def get_experiences_detail(self, request, slug):
        experiences_detail_queryset = self.get_object().experience_details
        experiences_detail_serializer = ExperienceSerializer(
            experiences_detail_queryset,
            many=True)

        return var_res.response_data(data=experiences_detail_serializer.data)

    @action(methods=["get"], detail=True,
            url_path="certificates-detail", url_name="get-certificates-detail")
    def get_certificates_detail(self, request, slug):
        certificates_detail_queryset = self.get_object().certificates
        certificates_detail_serializer = CertificateSerializer(
            certificates_detail_queryset,
            many=True)

        return var_res.response_data(data=certificates_detail_serializer.data)

    @action(methods=["get"], detail=True,
            url_path="language-skills", url_name="get-language-skills")
    def get_language_skills(self, request, slug):
        language_skill_queryset = self.get_object().language_skills
        language_skill_serializer = LanguageSkillSerializer(
            language_skill_queryset,
            many=True)

        return var_res.response_data(data=language_skill_serializer.data)

    @action(methods=["get"], detail=True,
            url_path="advanced-skills", url_name="get-advanced-skills")
    def get_advanced_skills(self, request, slug):
        advanced_skill_queryset = self.get_object().advanced_skills
        advanced_skill_serializer = AdvancedSkillSerializer(
            advanced_skill_queryset,
            many=True)

        return var_res.response_data(data=advanced_skill_serializer.data)


class ResumeViewSet(viewsets.ViewSet,
                    generics.ListAPIView,
                    generics.RetrieveAPIView):
    queryset = Resume.objects
    serializer_class = ResumeSerializer
    permission_classes = [perms_custom.IsEmployerUser]
    renderer_classes = [renderers.MyJSONRenderer]
    pagination_class = paginations.CustomPagination
    filterset_class = ResumeFilter
    filter_backends = [DjangoFilterBackend]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action in ["retrieve"]:
            return ResumeDetailSerializer
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(is_active=True)
                                        .order_by('-id', 'update_at', 'create_at'))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, fields=[
                'id', 'slug', 'title', 'salaryMin', 'salaryMax',
                'experience', 'viewEmployerNumber', 'updateAt',
                'userDict', 'jobSeekerProfileDict', 'city',
                'isSaved', 'type'
            ])
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return var_res.Response(serializer.data)

    @action(methods=["post"], detail=True,
            url_path="resume-saved", url_name="resume-saved")
    def resume_saved(self, request, slug):
        user = request.user
        saved_resumes = ResumeSaved.objects.filter(company=user.company, resume=self.get_object())
        is_saved = False
        if saved_resumes.exists():
            saved_resume = saved_resumes.first()

            saved_resume.delete()
        else:
            ResumeSaved.objects.create(
                company=request.user.company,
                resume=self.get_object()
            )
            is_saved = True
        # send notification
        company = user.company
        notification_content = "Đã lưu hồ sơ của bạn" if is_saved else "Đã hủy lưu hồ sơ của bạn"
        helper.add_employer_saved_resume_notifications(
            company.company_name,
            notification_content,
            company.company_image_url,
            self.get_object().user_id
        )
        return Response(data={
            "isSaved": is_saved
        })

    @action(methods=["post"], detail=True,
            url_path="view-resume", url_name="view-resume")
    def view_resume(self, request, slug):
        user = request.user
        v, _ = ResumeViewed.objects.get_or_create(
            resume=self.get_object(),
            company=user.company
        )
        try:
            v.views = F('views') + 1
            v.save()
            v.refresh_from_db()
            # send notification
            company = user.company
            helper.add_employer_viewed_resume_notifications(
                company.company_name,
                "Đã xem hồ sơ của bạn",
                company.company_image_url,
                self.get_object().user_id
            )
        except Exception as ex:
            helper.print_log_error("view_resume", ex)
            return var_res.Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return var_res.Response(status=status.HTTP_200_OK)


class ResumeViewedAPIView(views.APIView):
    permission_classes = [perms_custom.IsJobSeekerUser]
    renderer_classes = [renderers.MyJSONRenderer]
    pagination_class = paginations.CustomPagination

    # danh sach luot xem cua NTD doi voi ung vien hien tai
    def get(self, request):
        user = request.user

        queryset = ResumeViewed.objects.filter(
            resume__user=user
        ).order_by('-update_at', '-create_at')

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = ResumeViewedSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = ResumeViewedSerializer(queryset, many=True)
        return Response(data=serializer.data)


class ResumeSavedViewSet(viewsets.ViewSet,
                         generics.ListAPIView):
    queryset = ResumeSaved.objects
    permission_classes = [perms_custom.IsEmployerUser]
    renderer_classes = [renderers.MyJSONRenderer]
    pagination_class = paginations.CustomPagination
    serializer_class = ResumeSavedSerializer
    filterset_class = ResumeSavedFilter
    filter_backends = [DjangoFilterBackend]

    def list(self, request, *args, **kwargs):
        # danh sach ho so da luu cua nha tuyen dung
        user = request.user
        queryset = self.filter_queryset(self.get_queryset()
                                        .filter(company=user.company, resume__is_active=True)
                                        .order_by("-create_at"))

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = ResumeSavedSerializer(page, many=True, fields=[
                "id", "resume", "createAt"
            ])
            return paginator.get_paginated_response(serializer.data)

        serializer = ResumeSavedSerializer(queryset, many=True)
        return Response(data=serializer.data)

    @action(methods=["get"], detail=False,
            url_path="export", url_name="resumes-export")
    def export_resumes(self, request):
        user = request.user
        queryset = self.filter_queryset(self.get_queryset()
                                        .filter(company=user.company,
                                                resume__is_active=True)
                                        .order_by("-create_at"))
        serializer = ResumeSavedExportSerializer(queryset, many=True)

        result_data = utils.convert_data_with_en_key_to_vn_kew(serializer.data,
                                                               table_export.RESUMES_EXPORT_FIELD)
        return Response(data=result_data)


class EducationDetailViewSet(viewsets.ViewSet,
                             generics.CreateAPIView,
                             generics.RetrieveUpdateDestroyAPIView):
    queryset = EducationDetail.objects
    serializer_class = EducationSerializer
    renderer_classes = [renderers.MyJSONRenderer]


class ExperienceDetailViewSet(viewsets.ViewSet,
                              generics.CreateAPIView,
                              generics.RetrieveUpdateDestroyAPIView):
    queryset = ExperienceDetail.objects
    serializer_class = ExperienceSerializer
    renderer_classes = [renderers.MyJSONRenderer]


class CertificateDetailViewSet(viewsets.ViewSet,
                               generics.CreateAPIView,
                               generics.RetrieveUpdateDestroyAPIView):
    queryset = Certificate.objects
    serializer_class = CertificateSerializer
    renderer_classes = [renderers.MyJSONRenderer]


class LanguageSkillViewSet(viewsets.ViewSet,
                           generics.CreateAPIView,
                           generics.RetrieveUpdateDestroyAPIView):
    queryset = LanguageSkill.objects
    serializer_class = LanguageSkillSerializer
    renderer_classes = [renderers.MyJSONRenderer]


class AdvancedSkillViewSet(viewsets.ViewSet,
                           generics.CreateAPIView,
                           generics.RetrieveUpdateDestroyAPIView):
    queryset = AdvancedSkill.objects
    serializer_class = AdvancedSkillSerializer
    renderer_classes = [renderers.MyJSONRenderer]


class CompanyView(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ["get_company_info"]:
            return [perms_custom.IsEmployerUser()]
        return perms_sys.IsAuthenticated()

    def get_company_info(self, request):
        user = request.user
        try:
            company = Company.objects.get(user=user)
            company_serializer = CompanySerializer(company)
        except Exception as ex:
            helper.print_log_error("get_company_info", ex)
            return var_res.response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return var_res.response_data(data=company_serializer.data)

    def get_job_post_detail(self, request, pk):
        try:
            user = request.user
            job_post_queryset = JobPost.objects.get(pk=pk, user=user, company=user.company)

            job_post_serializer = job_serializers \
                .JobPostSerializer(job_post_queryset,
                                   fields=["id", "jobName", "academicLevel", "deadline", "quantity", "genderRequired",
                                           "jobDescription", "jobRequirement", "benefitsEnjoyed", "career",
                                           "position", "typeOfWorkplace", "experience",
                                           "jobType", "salaryMin", "salaryMax", "isUrgent",
                                           "contactPersonName", "contactPersonPhone", "contactPersonEmail",
                                           "location"])
        except JobPost.DoesNotExist:
            return var_res.response_data(data=None)
        except Exception as ex:
            helper.print_log_error("get_job_post_detail", ex)
            return var_res.response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return var_res.response_data(data=job_post_serializer.data)


class PrivateCompanyViewSet(viewsets.ViewSet,
                            generics.UpdateAPIView):
    queryset = Company.objects
    serializer_class = CompanySerializer
    permission_classes = [perms_custom.IsEmployerUser]
    renderer_classes = [renderers.MyJSONRenderer]

    @action(methods=["put"], detail=False,
            url_path="company-image-url", url_name="company-image-url")
    def update_company_image_url(self, request):
        files = request.FILES
        company_image_url_serializer = LogoCompanySerializer(request.user.company, data=files)
        if not company_image_url_serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            company_image_url_serializer.save()
        except Exception as ex:
            helper.print_log_error("update_company_image_url", ex)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_200_OK, data=company_image_url_serializer.data)

    @action(methods=["put"], detail=False,
            url_path="company-cover-image-url", url_name="company-cover-image-url")
    def update_company_cover_image_url(self, request):
        files = request.FILES
        company_cover_image_url_serializer = CompanyCoverImageSerializer(request.user.company, data=files)
        if not company_cover_image_url_serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            company_cover_image_url_serializer.save()
        except Exception as ex:
            helper.print_log_error("update_company_cover_image_url", ex)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_200_OK, data=company_cover_image_url_serializer.data)


class CompanyViewSet(viewsets.ViewSet,
                     generics.ListAPIView,
                     generics.RetrieveAPIView):
    queryset = Company.objects
    serializer_class = CompanySerializer
    permission_classes = [perms_sys.AllowAny]
    renderer_classes = [renderers.MyJSONRenderer]
    pagination_class = paginations.CustomPagination
    filterset_class = CompanyFilter
    filter_backends = [DjangoFilterBackend]
    lookup_field = "slug"

    def get_permissions(self):
        if self.action in ["followed"]:
            return [perms_custom.IsJobSeekerUser()]
        return [perms_sys.AllowAny()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()
                                        .order_by('-id', 'update_at', 'create_at'))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, fields=[
                'id', 'slug', 'companyName', 'companyImageUrl',
                'companyCoverImageUrl',
                'fieldOperation', 'employeeSize', 'locationDict',
                'followNumber', 'jobPostNumber', 'isFollowed'
            ])
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return var_res.Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, fields=[
            'id', 'slug', 'taxCode', 'companyName',
            'employeeSize', 'fieldOperation', 'location',
            'since', 'companyEmail', 'companyPhone',
            'websiteUrl', 'facebookUrl', 'youtubeUrl',
            'linkedinUrl', 'description',
            'companyImageUrl', 'companyCoverImageUrl',
            'followNumber', 'isFollowed', 'companyImages'
        ])
        return Response(data=serializer.data)

    @action(methods=["get"], detail=False,
            url_path="top", url_name="companies-top")
    def get_top_companies(self, request):
        try:
            queryset = Company.objects.annotate(num_follow=Count('companyfollowed'),
                                                num_job_post=Count('job_posts')
                                                ) \
                           .order_by('-num_follow', '-num_job_post')[:10]
            serializer = CompanySerializer(queryset, many=True,
                                           fields=[
                                               'id', 'slug', 'companyName', 'companyImageUrl'
                                           ])
        except Exception as ex:
            helper.print_log_error("get_top_companies", ex)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=serializer.data)

    @action(methods=["post"], detail=True,
            url_path="followed", url_name="followed")
    def followed(self, request, slug):
        user = request.user
        company = self.get_object()

        is_followed = False
        companies_followed = CompanyFollowed.objects.filter(user=user, company=company)
        if companies_followed.exists():
            company_followed = companies_followed.first()
            company_followed.delete()
        else:
            CompanyFollowed.objects.create(
                user=request.user,
                company=self.get_object(),
            )
            is_followed = True
        # send notification
        notification_title = f"{user.full_name} - {user.email}"
        notification_content = "Đã theo dõi bạn" if is_followed else "Đã hủy theo dõi bạn"
        helper.add_company_followed_notifications(
            notification_title,
            notification_content,
            user.avatar_url,
            company.user_id
        )
        return Response(data={
            "isFollowed": is_followed
        })


class CompanyFollowedAPIView(views.APIView):
    permission_classes = [perms_custom.IsJobSeekerUser]
    renderer_classes = [renderers.MyJSONRenderer]
    pagination_class = paginations.CustomPagination

    # danh sach cong ty dang follow
    def get(self, request):
        user = request.user

        queryset = CompanyFollowed.objects.filter(user=user) \
            .order_by("-update_at", "-create_at")

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = CompanyFollowedSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = CompanyFollowedSerializer(queryset, many=True)
        return Response(data=serializer.data)


class CompanyImageViewSet(viewsets.ViewSet,
                          generics.CreateAPIView,
                          generics.ListAPIView,
                          generics.DestroyAPIView):
    queryset = CompanyImage.objects
    serializer_class = CompanyImageSerializer
    pagination_class = paginations.CustomPagination
    renderer_classes = [renderers.MyJSONRenderer]
    permission_classes = [perms_custom.CompanyImageOwnerPerms]

    def get_queryset(self):
        queryset = self.queryset
        if self.request.user.is_authenticated:
            queryset = queryset.filter(company=self.request.user.company) \
                .order_by('update_at', 'create_at')

        return queryset

    def create(self, request, *args, **kwargs):
        files = request.FILES
        serializer = self.get_serializer(data=files)
        serializer.is_valid(raise_exception=True)
        results = serializer.save()
        return Response(results, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        image_public_id = instance.image_public_id
        if image_public_id:
            cloudinary.uploader.destroy(image_public_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=["POST"])
@permission_classes(permission_classes=[perms_custom.IsEmployerUser])
def send_email_reply_to_job_seeker(request):
    data = request.data
    user = request.user
    company = user.company

    serializer = SendMailReplyToJobSeekerSerializer(data=data)
    if not serializer.is_valid():
        return var_res.response_data(status=status.HTTP_400_BAD_REQUEST,
                                     errors=serializer.errors)
    validate_data = serializer.data

    to = [validate_data.get("email")]
    is_send_me = validate_data.pop("isSendMe")
    if is_send_me:
        to.append(user.email)

    email_data = {
        'content': validate_data.get("content"),
        'company_image': company.company_image_url,
        'company_name': company.company_name,
        'company_phone': company.company_phone,
        'company_email': company.company_email,
        'company_address': company.location.address,
        'company_website_url': company.website_url
    }
    queue_mail.send_email_reply_job_seeker_task.delay(
        to=to,
        subject=validate_data.get("title"),
        data=email_data
    )
    return var_res.response_data()

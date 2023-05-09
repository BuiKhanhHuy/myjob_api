from configs import variable_system as var_sys
from configs import variable_response as var_res, renderers, paginations
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from helpers import helper
from rest_framework import viewsets, generics, views
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions as perms_sys
from authentication import permissions as perms_custom
from rest_framework import status
from ..models import (
    JobSeekerProfile,
    Resume, ResumeViewed,
    EducationDetail, ExperienceDetail,
    Certificate, LanguageSkill,
    AdvancedSkill, Company,
    CompanyFollowed,
)
from ..filters import (
    CompanyFilter
)
from ..serializers import (
    JobSeekerProfileSerializer,
    ResumeSerializer,
    ResumeViewedSerializer,
    CvSerializer,
    EducationSerializer,
    ExperienceSerializer,
    CertificateSerializer,
    LanguageSkillSerializer,
    AdvancedSkillSerializer,
    CompanySerializer,
    CompanyFollowedSerializer,
)


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
                "id", "title", "type"
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
                                              fields=["id", "title", "experience", "position",
                                                      "salaryMin", "salaryMax", "updateAt",
                                                      "user", "isActive"])
            else:
                serializer = ResumeSerializer(resumes, many=True,
                                              fields=["id", "title", "updateAt",
                                                      "imageUrl", "fileUrl", "isActive"])

        return var_res.response_data(data=serializer.data)


class PrivateResumeViewSet(viewsets.ViewSet,
                           generics.CreateAPIView,
                           generics.UpdateAPIView,
                           generics.DestroyAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

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
                                             "id", "title", "description",
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
    def active_resume(self, request, pk):
        resume = self.get_object()
        if resume.is_active:
            resume.is_active = False
            resume.save()
            return var_res.response_data(data={
                "isActive": False
            })
        else:
            Resume.objects.filter(user=self.request.user) \
                .exclude(slug=resume.slug) \
                .update(is_active=False)
            resume.is_active = True
            resume.save()
            return var_res.response_data(data={
                "isActive": True
            })

    @action(methods=["get"], detail=True,
            url_path='resume-owner', url_name="get-resume-detail-of-job-seeker", )
    def get_resume_detail_of_job_seeker(self, request, pk):
        resume_queryset = self.get_object()
        resume_serializer = ResumeSerializer(resume_queryset,
                                             fields=["id", "title", "salaryMin", "salaryMax",
                                                     "position", "experience", "academicLevel",
                                                     "typeOfWorkplace", "jobType", "description",
                                                     "isActive", "city", "career"])

        return var_res.response_data(data=resume_serializer.data)

    @action(methods=["get"], detail=True,
            url_path='cv', url_name="get-cv", )
    def get_cv(self, request, pk):
        resume_queryset = self.get_object()
        resume_serializer = CvSerializer(resume_queryset,
                                         fields=["id", "title", "fileUrl", "updateAt"])

        return var_res.response_data(data=resume_serializer.data)

    @get_cv.mapping.put
    def update_cv_file(self, request, pk):
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
    def get_educations_detail(self, request, pk):
        educations_detail_queryset = self.get_object().education_details
        educations_detail_serializer = EducationSerializer(
            educations_detail_queryset,
            many=True)

        return var_res.response_data(data=educations_detail_serializer.data)

    @action(methods=["get"], detail=True,
            url_path="experiences-detail", url_name="get-experiences-detail")
    def get_experiences_detail(self, request, pk):
        experiences_detail_queryset = self.get_object().experience_details
        experiences_detail_serializer = ExperienceSerializer(
            experiences_detail_queryset,
            many=True)

        return var_res.response_data(data=experiences_detail_serializer.data)

    @action(methods=["get"], detail=True,
            url_path="certificates-detail", url_name="get-certificates-detail")
    def get_certificates_detail(self, request, pk):
        certificates_detail_queryset = self.get_object().certificates
        certificates_detail_serializer = CertificateSerializer(
            certificates_detail_queryset,
            many=True)

        return var_res.response_data(data=certificates_detail_serializer.data)

    @action(methods=["get"], detail=True,
            url_path="language-skills", url_name="get-language-skills")
    def get_language_skills(self, request, pk):
        language_skill_queryset = self.get_object().language_skills
        language_skill_serializer = LanguageSkillSerializer(
            language_skill_queryset,
            many=True)

        return var_res.response_data(data=language_skill_serializer.data)

    @action(methods=["get"], detail=True,
            url_path="advanced-skills", url_name="get-advanced-skills")
    def get_advanced_skills(self, request, pk):
        advanced_skill_queryset = self.get_object().advanced_skills
        advanced_skill_serializer = AdvancedSkillSerializer(
            advanced_skill_queryset,
            many=True)

        return var_res.response_data(data=advanced_skill_serializer.data)


class ResumeViewedAPIView(views.APIView):
    permission_classes = [perms_custom.IsJobSeekerUser]
    renderer_classes = [renderers.MyJSONRenderer]
    pagination_class = paginations.CustomPagination

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
                'id', 'companyName', 'companyImageUrl',
                'followNumber', 'jobPostNumber', 'isFollowed'
            ])
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return var_res.Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, fields=[
            'id', 'taxCode', 'companyName',
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
                           .exclude(Q(company_image_public_id__isnull=True)
                                    | Q(website_url__isnull=True)
                                    | Q(field_operation__isnull=True)
                                    | Q(employee_size__isnull=True)
                                    | Q(since__isnull=True)) \
                           .order_by('-num_follow', '-num_job_post')[:10]
            serializer = CompanySerializer(queryset, many=True,
                                           fields=[
                                               'id', 'companyName', 'companyImageUrl',
                                               'followNumber', 'jobPostNumber', 'isFollowed'
                                           ], context={'request': request})
        except Exception as ex:
            helper.print_log_error("get_top_companies", ex)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=serializer.data)

    @action(methods=["post"], detail=True,
            url_path="followed", url_name="followed")
    def followed(self, request, pk):
        is_followed = False
        companies_followed = CompanyFollowed.objects.filter(user=request.user, company=self.get_object())
        if companies_followed.exists():
            company_followed = companies_followed.first()
            company_followed.delete()
        else:
            CompanyFollowed.objects.create(
                user=request.user,
                company=self.get_object(),
            )
            is_followed = True
        return Response(data={
            "isFollowed": is_followed
        })


class CompanyFollowedAPIView(views.APIView):
    permission_classes = [perms_custom.IsJobSeekerUser]
    renderer_classes = [renderers.MyJSONRenderer]
    pagination_class = paginations.CustomPagination

    def get(self, request):
        user = request.user

        queryset = CompanyFollowed.objects.filter(user=user) \
            .order_by("-update_at", "-create_at")

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = CompanyFollowedSerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        serializer = CompanyFollowedSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data)

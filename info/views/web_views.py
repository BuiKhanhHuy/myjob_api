import cloudinary.uploader
import cloudinary.api
from io import BytesIO
from PIL import Image

from configs import variable_system as var_sys
from configs import variable_response as var_res, renderers
from helpers import helper
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework import permissions as perms_sys
from authentication import permissions as perms_custom
from rest_framework import status
from ..models import (
    JobSeekerProfile, Resume,
    EducationDetail, ExperienceDetail,
    Certificate, LanguageSkill,
    AdvancedSkill, Company)
from ..serializers import (
    JobSeekerProfileSerializer,
    ResumeSerializer,
    CvSerializer,
    EducationSerializer,
    ExperienceSerializer,
    CertificateSerializer,
    LanguageSkillSerializer,
    AdvancedSkillSerializer,
    CompanySerializer,
)
from job.models import (
    JobPost
)
from job import serializers as job_serializers



class ProfileView(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ["get_profile_info",
                           "update_profile_info",
                           "get_profile_info_detail"]:
            return [perms_custom.IsJobSeekerUser()]
        return [perms_sys.IsAuthenticated()]

    def get_profile_info(self, request):
        user = request.user
        try:
            profile = JobSeekerProfile.objects.get(user_id__exact=user.id)
            profile_serializer = JobSeekerProfileSerializer(profile)
        except Exception as ex:
            helper.print_log_error("get_profile_info", ex)
            return var_res.response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return var_res.response_data(data=profile_serializer.data)

    def update_profile_info(self, request):
        data = request.data

        try:
            job_seeker_profile = request.user.job_seeker_profile

            serializer = JobSeekerProfileSerializer(job_seeker_profile, data=data)
            if not serializer.is_valid():
                return var_res.response_data(status=status.HTTP_400_BAD_REQUEST,
                                             errors=serializer.errors)
            serializer.save()
        except Exception as ex:
            helper.print_log_error("update_profile_info", ex)
            return var_res.response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return var_res.response_data(data=serializer.data)


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
        if "resumeType" not in query_params:
            return var_res.response_data(status=status.HTTP_400_BAD_REQUEST,
                                         errors={"detail": "resumeType is required."})
        resume_type = query_params["resumeType"]
        if not (resume_type == var_sys.CV_WEBSITE) and not (resume_type == var_sys.CV_UPLOAD):
            return var_res.response_data(status=status.HTTP_400_BAD_REQUEST,
                                         errors={"detail": "resumeType is invalid."})

        job_seeker_profile = self.get_object()
        if not job_seeker_profile:
            raise Exception("User doesn't have job_seeker_profile.")

        resumes = job_seeker_profile.resumes
        resumes = resumes.filter(type=resume_type)
        if resume_type == var_sys.CV_WEBSITE:
            if not resumes.first():
                return var_res.response_data()
            serializer = ResumeSerializer(resumes.first(),
                                          fields=["id", "slug", "title", "experience", "position",
                                                  "salaryMin", "salaryMax", "updateAt", "user"])
        else:
            serializer = ResumeSerializer(resumes, many=True,
                                          fields=["id", "slug", "title", "updateAt",
                                                  "imageUrl", "fileUrl"])

        return var_res.response_data(data=serializer.data)


class ResumeViewSet(viewsets.ViewSet,
                    generics.ListCreateAPIView,
                    generics.RetrieveUpdateDestroyAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ["get_resume_detail_of_job_seeker",
                           "update", "partial_update",
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
        if self.action in ["get_company_info", "get_job_posts",
                           "get_job_post_detail"]:
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

    def get_job_posts(self, request):
        try:
            user = request.user

            job_posts_queryset = JobPost.objects.filter(user=user, company=user.company)

            job_posts_serializer = job_serializers \
                .JobPostSerializer(job_posts_queryset,
                                   many=True,
                                   fields=["id", "slug", "jobName", "createAt", "deadline",
                                           "appliedNumber", "viewedNumber", "isUrgent"])
        except Exception as ex:
            helper.print_log_error("get_job_post", ex)
            return var_res.response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return var_res.response_data(data=job_posts_serializer.data)

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


class CompanyViewSet(viewsets.ViewSet,
                     generics.ListAPIView,
                     generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects
    # mai mốt đổi lại của list
    serializer_class = CompanySerializer
    permission_classes = [perms_sys.AllowAny()]
    renderer_classes = [renderers.MyJSONRenderer]

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [perms_custom.IsEmployerUser()]
        return self.get_permissions()

    def get_serializer_class(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return CompanySerializer
        return self.serializer_class

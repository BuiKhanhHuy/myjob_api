from configs import variable_system as var_sys
from django.db import models
from .base import InfoBaseModel
from authentication.models import User
from common.models import Career, Skill, Location


class JobSeekerProfile(InfoBaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    marital_status = models.CharField(max_length=1,
                                      choices=var_sys.MARITAL_STATUS_CHOICES,
                                      default=var_sys.MARITAL_STATUS_CHOICES[0][0])
    experience = models.SmallIntegerField(choices=var_sys.EXPERIENCE_CHOICES)

    # OneToOneField
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="job_seeker_profile")
    # ForeignKey
    career = models.ForeignKey(Career, on_delete=models.SET_NULL, null=True, related_name="job_seeker_profiles")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name="job_seeker_profiles")
    # ManyToManyField
    skills = models.ManyToManyField(Skill, through="SeekerProfileSkill", related_name="job_seeker_profiles")

    class Meta:
        db_table = "myjob_info_job_seeker_profile"


class EducationDetail(InfoBaseModel):
    degree_name = models.CharField(max_length=200)
    major = models.CharField(max_length=255)
    training_place_name = models.CharField(max_length=255)
    start_date = models.DateField()
    completed_date = models.DateField(null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    # ForeignKey
    job_seeker_profile = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name="education_details")

    class Meta:
        db_table = "myjob_info_education_detail"


class ExperienceDetail(InfoBaseModel):
    job_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.CharField(max_length=255, null=True, blank=True)
    position = models.SmallIntegerField(var_sys.POSITION_CHOICES)

    # ForeignKey
    job_seeker_profile = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE,
                                           related_name="experience_details")

    class Meta:
        db_table = "myjob_info_experience_detail"


class Appreciation(InfoBaseModel):
    award_name = models.CharField(max_length=200)
    category = models.CharField(max_length=255)
    end_date = models.DateField()
    description = models.CharField(max_length=255, null=True, blank=True)

    # ForeignKey
    job_seeker_profile = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE,
                                           related_name="appreciations")

    class Meta:
        db_table = "myjob_info_appreciation"


class LanguageSkill(InfoBaseModel):
    language = models.SmallIntegerField(choices=var_sys.LANGUAGE_CHOICES)
    first_language = models.BooleanField(default=False)
    level = models.SmallIntegerField(choices=var_sys.LANGUAGE_LEVEL_CHOICES)
    description = models.CharField(max_length=255, null=True, blank=True)

    # ForeignKey
    job_seeker_profile = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE,
                                           related_name="language_skills")

    class Meta:
        db_table = "myjob_info_language_skill"


class SeekerProfileSkill(InfoBaseModel):
    # Foreignkey
    job_seeker_profile = models.ForeignKey("JobSeekerProfile", on_delete=models.CASCADE,
                                           related_name="seeker_profile_skills")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE,
                              related_name="seeker_profile_skills")

    class Meta:
        db_table = "myjob_info_seeker_profile_skill"

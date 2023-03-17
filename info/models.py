from configs import variable_system as var_sys
from django.db import models
from authentication.models import User
from common.models import Career, City, District, Location


class InfoBaseModel(models.Model):
    class Meta:
        abstract = True

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Company(InfoBaseModel):
    company_name = models.CharField(max_length=255, unique=True)
    company_image_url = models.URLField(default=var_sys.AVATAR_DEFAULT["LOGO"])
    company_email = models.EmailField(max_length=100, unique=True)
    company_phone = models.CharField(max_length=15, unique=True)
    website_url = models.URLField(max_length=300, null=True, blank=True)
    tax_code = models.CharField(max_length=30, unique=True)
    since = models.DateField(null=True)
    field_operation = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    employee_size = models.SmallIntegerField(choices=var_sys.EMPLOYEE_SIZE_CHOICES, null=True)

    # OneToOneField
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name="company")
    # ForeignKey
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True,
                                 related_name="companies")

    class Meta:
        db_table = "myjob_info_company"


class CompanyImage(InfoBaseModel):
    image_url = models.URLField(max_length=300)
    index = models.SmallIntegerField()

    # ForeignKey
    company = models.ForeignKey("Company", on_delete=models.CASCADE,
                                related_name="company_images")

    class Meta:
        db_table = "myjob_info_company_image"


class JobSeekerProfile(InfoBaseModel):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    cover_image_url = models.URLField(max_length=300, default=var_sys.AVATAR_DEFAULT["COVER_IMG"])
    phone = models.CharField(max_length=15, blank=True, null=True)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=var_sys.GENDER_CHOICES, null=True)
    marital_status = models.CharField(max_length=1,
                                      choices=var_sys.MARITAL_STATUS_CHOICES,
                                      default=var_sys.MARITAL_STATUS_CHOICES[0][0],
                                      null=True)
    is_active = models.BooleanField(default=False)

    # OneToOneField
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="job_seeker_profile")
    # ForeignKey
    career = models.ForeignKey(Career, on_delete=models.SET_NULL, null=True, related_name="job_seeker_profiles")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True,
                                 related_name="job_seeker_profiles")

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


class Certificate(InfoBaseModel):
    name = models.CharField(max_length=200)
    training_place = models.CharField(max_length=255)
    start_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)

    # ForeignKey
    job_seeker_profile = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE,
                                           related_name='certificates')

    class Meta:
        db_table = "myjob_info_certificate"


class LanguageSkill(InfoBaseModel):
    language = models.SmallIntegerField(choices=var_sys.LANGUAGE_CHOICES)
    level = models.SmallIntegerField(choices=var_sys.LANGUAGE_LEVEL_CHOICES)

    # ForeignKey
    job_seeker_profile = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE,
                                           related_name="language_skills")

    class Meta:
        db_table = "myjob_info_language_skill"


class AdvancedSkill(InfoBaseModel):
    name = models.CharField(max_length=200)
    level = models.SmallIntegerField(default=3)

    job_seeker_profile = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE,
                                           related_name='advanced_skills')

    class Meta:
        db_table = "myjob_info_advanced_skill"

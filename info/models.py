from configs import variable_system as var_sys
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField
from authentication.models import User
from common.models import (
    Career, City, District, Location,
)


class InfoBaseModel(models.Model):
    class Meta:
        abstract = True

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class JobSeekerProfile(InfoBaseModel):
    phone = models.CharField(max_length=15, blank=True, null=True)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=var_sys.GENDER_CHOICES, null=True)
    marital_status = models.CharField(max_length=1,
                                      choices=var_sys.MARITAL_STATUS_CHOICES,
                                      default=var_sys.MARITAL_STATUS_CHOICES[0][0],
                                      null=True)
    # OneToOneField
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="job_seeker_profile")
    # ForeignKey
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True,
                                 related_name="job_seeker_profiles")

    class Meta:
        db_table = "myjob_info_job_seeker_profile"

    def __str__(self):
        return f'Job seeker profile of {self.user.email}'


class Resume(InfoBaseModel):
    title = models.CharField(max_length=200, null=True)
    slug = AutoSlugField(populate_from='title',
                         unique=True,
                         unique_with=['id'],
                         slugify=slugify)
    # slug = AutoSlugField(populate_from='title', unique=True, slugify_function=slugify)
    description = models.TextField(null=True)
    salary_min = models.DecimalField(default=0, max_digits=12, decimal_places=0)
    salary_max = models.DecimalField(default=0, max_digits=12, decimal_places=0)
    position = models.SmallIntegerField(choices=var_sys.POSITION_CHOICES, null=True)
    experience = models.SmallIntegerField(choices=var_sys.EXPERIENCE_CHOICES, null=True)
    academic_level = models.SmallIntegerField(choices=var_sys.ACADEMIC_LEVEL, null=True)
    type_of_workplace = models.SmallIntegerField(choices=var_sys.TYPE_OF_WORKPLACE_CHOICES, null=True)
    job_type = models.SmallIntegerField(choices=var_sys.JOB_TYPE_CHOICES, null=True)
    is_active = models.BooleanField(default=False)

    image_url = models.URLField(null=True)
    file_url = models.URLField(null=True)
    public_id = models.CharField(null=True, max_length=255)
    type = models.CharField(max_length=10, default=var_sys.CV_UPLOAD)

    # ForeignKey
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name="resumes")
    career = models.ForeignKey(Career, on_delete=models.SET_NULL, null=True, related_name="resumes")
    job_seeker_profile = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name="resumes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resumes")

    # ManyToManyField
    company_viewers = models.ManyToManyField("Company", through='ResumeViewed', related_name="resumes_viewed")
    company_savers = models.ManyToManyField("Company", through='ResumeSaved', related_name="resumes_saved")

    class Meta:
        db_table = "myjob_info_resume"

    def __str__(self):
        return f"{self.title} - {self.user}"


class EducationDetail(InfoBaseModel):
    degree_name = models.CharField(max_length=200)
    major = models.CharField(max_length=255)
    training_place_name = models.CharField(max_length=255)
    start_date = models.DateField()
    completed_date = models.DateField(null=True)
    description = models.CharField(max_length=500, blank=True, null=True)

    # ForeignKey
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="education_details")

    class Meta:
        db_table = "myjob_info_education_detail"


class ExperienceDetail(InfoBaseModel):
    job_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.CharField(max_length=500, null=True, blank=True)

    # ForeignKey
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE,
                               related_name="experience_details")

    class Meta:
        db_table = "myjob_info_experience_detail"


class Certificate(InfoBaseModel):
    name = models.CharField(max_length=200)
    training_place = models.CharField(max_length=255)
    start_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)

    # ForeignKey
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE,
                               related_name='certificates')

    class Meta:
        db_table = "myjob_info_certificate"


class LanguageSkill(InfoBaseModel):
    language = models.SmallIntegerField(choices=var_sys.LANGUAGE_CHOICES)
    level = models.SmallIntegerField(choices=var_sys.LANGUAGE_LEVEL_CHOICES)

    # ForeignKey
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE,
                               related_name="language_skills")

    class Meta:
        db_table = "myjob_info_language_skill"


class AdvancedSkill(InfoBaseModel):
    name = models.CharField(max_length=200)
    level = models.SmallIntegerField(default=3)

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE,
                               related_name='advanced_skills')

    class Meta:
        db_table = "myjob_info_advanced_skill"


class CompanyFollowed(InfoBaseModel):
    # ForeignKey
    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "myjob_info_company_followed"
        verbose_name_plural = "Companies followed"

    def __str__(self):
        return f"{self.user} followed {self.company}"


class Company(InfoBaseModel):
    company_name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='company_name', unique=True,
                         unique_with=['id'],
                         slugify=slugify, max_length=300)
    company_image_url = models.URLField(default=var_sys.AVATAR_DEFAULT["COMPANY_LOGO"])
    company_image_public_id = models.CharField(max_length=300, null=True)
    company_cover_image_url = models.URLField(default=var_sys.AVATAR_DEFAULT["COMPANY_COVER_IMAGE"])
    company_cover_image_public_id = models.CharField(max_length=300, null=True)
    facebook_url = models.URLField(null=True, blank=True)
    youtube_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    company_email = models.EmailField(max_length=100, unique=True)
    company_phone = models.CharField(max_length=15, unique=True)
    website_url = models.URLField(max_length=300, null=True, blank=True)
    tax_code = models.CharField(max_length=30, unique=True)
    since = models.DateField(null=True)
    field_operation = models.CharField(max_length=255, blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    employee_size = models.SmallIntegerField(choices=var_sys.EMPLOYEE_SIZE_CHOICES, null=True)

    # OneToOneField
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name="company")
    # ForeignKey
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True,
                                 related_name="companies")

    # ManyToManyField
    followers = models.ManyToManyField(User, through='CompanyFollowed', related_name="companies_followed")

    class Meta:
        db_table = "myjob_info_company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return f"{self.company_name if self.company_name is not None else '-'}"


class CompanyImage(InfoBaseModel):
    image_url = models.URLField(max_length=300)
    image_public_id = models.CharField(max_length=300, null=True)

    # ForeignKey
    company = models.ForeignKey("Company", on_delete=models.CASCADE,
                                related_name="company_images")

    class Meta:
        db_table = "myjob_info_company_image"


class ResumeSaved(InfoBaseModel):
    # ForeignKey
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = "myjob_info_resume_saved"
        verbose_name_plural = "Resumes saved"

    def __str__(self):
        return f"{self.company} saved {self.resume}"


class ResumeViewed(InfoBaseModel):
    views = models.BigIntegerField(default=0)

    # ForeignKey
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = "myjob_info_resume_viewed"
        verbose_name_plural = "Resumes viewed"

    def __str__(self):
        return f"{self.company} have watching {self.resume}"


class ContactProfile(InfoBaseModel):
    # ForeignKey
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = "myjob_info_contact_profile"
        verbose_name_plural = "Contact profiles"

    def __str__(self):
        return f"{self.company} saved {self.resume}"

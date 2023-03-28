from configs import variable_system as var_sys
from django.db import models
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField
from authentication.models import User
from common.models import City, District, Location, Career
from info.models import Company


class JobPostBaseModel(models.Model):
    class Meta:
        abstract = True

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class JobPost(JobPostBaseModel):
    job_name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='job_name', unique=True, slugify_function=slugify)
    deadline = models.DateField()
    quantity = models.IntegerField()
    gender_required = models.CharField(max_length=1, choices=var_sys.GENDER_CHOICES,
                                       blank=True, null=True)
    job_description = models.TextField()
    job_requirement = models.TextField(null=True, blank=True)
    benefits_enjoyed = models.TextField(null=True, blank=True)

    position = models.SmallIntegerField(choices=var_sys.POSITION_CHOICES)
    type_of_workplace = models.SmallIntegerField(choices=var_sys.TYPE_OF_WORKPLACE_CHOICES)
    experience = models.SmallIntegerField(choices=var_sys.EXPERIENCE_CHOICES)
    academic_level = models.SmallIntegerField(choices=var_sys.ACADEMIC_LEVEL)
    job_type = models.SmallIntegerField(choices=var_sys.JOB_TYPE_CHOICES)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    is_hot = models.BooleanField(default=False)
    is_urgent = models.BooleanField(default=False)
    contact_person_name = models.CharField(max_length=100)
    contact_person_phone = models.CharField(max_length=15)
    contact_person_email = models.EmailField(max_length=100)

    views = models.BigIntegerField(default=0)
    shares = models.BigIntegerField(default=0)

    # ForeignKey
    career = models.ForeignKey(Career, on_delete=models.SET_NULL,
                               related_name="job_posts", null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True,
                                 related_name="job_posts")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="job_posts")
    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                related_name="job_posts")

    class Meta:
        db_table = "myjob_job_job_post"


class SavedJobPost(JobPostBaseModel):
    # ForeignKey
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE,
                                 related_name="saved_job_posts")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="saved_job_posts")

    class Meta:
        db_table = "myjob_job_saved_job_post"


class JobPostActivity(JobPostBaseModel):
    # ForeignKey
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE,
                                 related_name="job_posts_activity")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="job_posts_activity")

    class Meta:
        db_table = "myjob_job_job_post_activity"

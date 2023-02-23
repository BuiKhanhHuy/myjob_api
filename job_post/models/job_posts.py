from configs import variable_system as var_sys
from django.db import models
from .base import JobPostBaseModel
from authentication.models import User
from common.models import Location, Career
from info.models import Company


class JobPost(JobPostBaseModel):
    job_name = models.CharField(max_length=255)
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
    job_type = models.SmallIntegerField(choices=var_sys.JOB_TYPE_CHOICES)

    # ForeignKey
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True,
                                 related_name="job_posts")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="job_posts")
    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                related_name="job_posts")

    # ManyToManyField
    careers = models.ManyToManyField(Career, through="JobPostCareer",
                                     related_name="job_posts")

    class Meta:
        db_table = "myjob_job_post_job_post"


class SavedJobPost(JobPostBaseModel):
    # ForeignKey
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE,
                                 related_name="saved_job_posts")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="saved_job_posts")

    class Meta:
        db_table = "myjob_job_post_saved_job_post"


class JobPostActivity(JobPostBaseModel):
    # ForeignKey
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE,
                                 related_name="job_posts_activity")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="job_posts_activity")

    class Meta:
        db_table = "myjob_job_post_job_post_activity"


class JobPostCareer(JobPostBaseModel):
    # ForeignKey
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE,
                                 related_name="job_post_careers")
    career = models.ForeignKey(Career, on_delete=models.CASCADE,
                               related_name="job_post_careers")

    class Meta:
        db_table = "myjob_job_post_job_post_career"

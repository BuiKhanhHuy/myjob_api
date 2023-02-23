from django.db import models
from .base import CommonBaseModel


class Career(CommonBaseModel):
    name = models.CharField(max_length=150)

    class Meta:
        db_table = "myjob_common_career"


class Skill(CommonBaseModel):
    name = models.CharField(max_length=150)

    class Meta:
        db_table = "myjob_common_skill"

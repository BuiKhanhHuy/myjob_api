from django.db import models
from .base import AuthBaseModel
from configs import variable_system as var_sys


class Role(AuthBaseModel):
    name = models.CharField(max_length=15, choices=var_sys.ROLE_CHOICES)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'myjob_authentication_role'

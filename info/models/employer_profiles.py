from configs import variable_system as var_sys
from django.db import models
from .base import InfoBaseModel
from authentication.models import User
from common.models import Location


class Company(InfoBaseModel):
    company_name = models.CharField(max_length=255, unique=True)
    company_image_url = models.URLField(default=var_sys.AVATAR_DEFAULT["LOGO"])
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=15, unique=True)
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

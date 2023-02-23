from django.db import models
from .base import CommonBaseModel


class City(CommonBaseModel):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = "myjob_common_city"


class District(CommonBaseModel):
    name = models.CharField(max_length=50)

    # ForeignKey
    city = models.ForeignKey('City', on_delete=models.CASCADE, related_name="districts")

    class Meta:
        db_table = "myjob_common_district"


class Location(CommonBaseModel):
    address = models.CharField(max_length=255, blank=True, null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    # ForeignKey
    district = models.ForeignKey("District", on_delete=models.CASCADE, related_name="locations")

    class Meta:
        db_table = "myjob_common_location"

from django.db import models
from django.db.models import Func, F
from math import radians, cos, sin, asin, sqrt
from authentication.models import User


class Haversine(Func):
    function = 'SELECT ST_Distance_Sphere(Point(%s,%s),Point(%s,%s))'
    output_field = models.DecimalField()

    def __init__(self, lat1, lon1, lat2, lon2, **kwargs):
        self.lat1, self.lon1, self.lat2, self.lon2 = lat1, lon1, lat2, lon2
        super().__init__(self.lat1, self.lon1, self.lat2, self.lon2, **kwargs)

    def as_sql(self, compiler, connection):
        return self.function, (radians(float(self.lat1)), radians(float(self.lon1)), radians(float(self.lat2)),
                               radians(float(self.lon2))), self.output_field


class CommonBaseModel(models.Model):
    class Meta:
        abstract = True

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


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
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True,
                             related_name="locations")
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True,
                                 related_name="locations")
    address = models.CharField(max_length=255, blank=True, null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    class Meta:
        db_table = "myjob_common_location"


class Career(CommonBaseModel):
    name = models.CharField(max_length=150)
    icon_url = models.URLField(max_length=300)

    class Meta:
        db_table = "myjob_common_career"

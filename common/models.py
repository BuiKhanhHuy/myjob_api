from django.db import models
from django.conf import settings


class CommonBaseModel(models.Model):
    class Meta:
        abstract = True

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class City(CommonBaseModel):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = "myjob_common_city"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class District(CommonBaseModel):
    name = models.CharField(max_length=50)

    # ForeignKey
    city = models.ForeignKey('City', on_delete=models.CASCADE, related_name="districts")

    class Meta:
        db_table = "myjob_common_district"

    def __str__(self):
        return self.name


class Location(CommonBaseModel):
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True,
                             related_name="locations")
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True,
                                 related_name="locations")
    address = models.CharField(max_length=255, blank=True, null=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "myjob_common_location"

    def __str__(self):
        return f"{self.city.name} - {self.district.name} - {self.address}"


class Career(CommonBaseModel):
    name = models.CharField(max_length=150)
    icon_url = models.URLField(max_length=300)
    app_icon_name = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "myjob_common_career"

    def __str__(self):
        return self.name


class File(CommonBaseModel):
    RESOURCE_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('raw', 'Raw File'),
    ]

    public_id = models.CharField(max_length=255, unique=True)
    version = models.CharField(max_length=20, null=True, blank=True)
    format = models.CharField(max_length=50)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    uploaded_at = models.DateTimeField(null=False, blank=False)
    bytes = models.IntegerField(default=0)
    metadata = models.JSONField(blank=True, null=True)
    
    def get_full_url(self):
        return f"{settings.CLOUDINARY_PATH.format(self.version) + self.public_id}.{self.format}"

    class Meta:
        db_table = "myjob_files"
        ordering = ['-create_at']
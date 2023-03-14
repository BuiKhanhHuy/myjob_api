from django.db import models


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


class Career(CommonBaseModel):
    name = models.CharField(max_length=150)

    class Meta:
        db_table = "myjob_common_career"


class Skill(CommonBaseModel):
    name = models.CharField(max_length=150)

    class Meta:
        db_table = "myjob_common_skill"

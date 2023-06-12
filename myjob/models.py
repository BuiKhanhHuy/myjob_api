from configs import variable_system as var_sys
from django.db import models
from authentication.models import User


class MyJobBaseModel(models.Model):
    class Meta:
        abstract = True

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Feedback(MyJobBaseModel):
    content = models.CharField(max_length=500)
    rating = models.SmallIntegerField(default=5)
    is_active = models.BooleanField(default=False)

    # ForeignKey
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedbacks")

    class Meta:
        db_table = "myjob_myjob_feedback"

    def __str__(self):
        return self.content


class Banner(MyJobBaseModel):
    image_url = models.URLField(null=True, blank=True)
    image_mobile_url = models.URLField(null=True, blank=True)
    button_text = models.TextField(max_length=20, null=True, blank=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    button_link = models.URLField(null=True, blank=True)
    is_show_button = models.BooleanField(default=False)
    description_location = models.IntegerField(choices=var_sys.DESCRIPTION_LOCATION,
                                               default=var_sys.DESCRIPTION_LOCATION[2][0])
    platform = models.CharField(max_length=3, choices=var_sys.PLATFORM_CHOICES,
                                default=var_sys.DESCRIPTION_LOCATION[0][0])
    type = models.IntegerField(choices=var_sys.BANNER_TYPE,
                               default=var_sys.BANNER_TYPE[0][0])
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = "myjob_myjob_banner"

    def __str__(self):
        return str(self.id)

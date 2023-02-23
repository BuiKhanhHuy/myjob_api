from django.db import models


class JobPostBaseModel(models.Model):
    class Meta:
        abstract = True
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

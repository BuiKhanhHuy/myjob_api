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

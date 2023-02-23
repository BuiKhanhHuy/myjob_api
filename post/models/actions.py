from django.db import models
from .base import PostBaseModel
from authentication.models import User


class Like(PostBaseModel):
    is_like = models.BooleanField(default=True)

    # ForeignKey
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey("post.Post", on_delete=models.CASCADE, related_name="likes")

    class Meta:
        db_table = "myjob_post_like"


class Comment(PostBaseModel):
    content = models.CharField(max_length=255)

    # ForeignKey
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey("post.Post", on_delete=models.CASCADE, related_name="comments")

    class Meta:
        db_table = "myjob_post_comment"


class SavedPost(PostBaseModel):
    # ForeignKey
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_posts")
    post = models.ForeignKey("post.Post", on_delete=models.CASCADE, related_name="saved_posts")

    class Meta:
        db_table = "myjob_post_saved_post"

from django.db import models
from .base import PostBaseModel
from authentication.models import User


class Post(PostBaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField()

    # ForeignKey
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_posts")
    # ManyToManyField
    commentators = models.ManyToManyField(User, through='post.Comment', related_name="commented_posts")
    liked_peoples = models.ManyToManyField(User, through='post.Like', related_name='liked_posts')
    saved_peoples = models.ManyToManyField(User, through='post.SavedPost', related_name='author_saved_posts')

    class Meta:
        db_table = "myjob_post_post"

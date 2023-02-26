from django.db import models
from authentication.models import User


class PostBaseModel(models.Model):
    class Meta:
        abstract = True

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


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

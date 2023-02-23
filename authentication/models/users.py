from django.contrib.auth.models import (AbstractUser, BaseUserManager)
from django.db import models
from helpers import utils


class UserManager(BaseUserManager):
    def create_user(self, email, full_name=utils.generate_random_name(), password=None):
        if email is None:
            raise TypeError('Users should have a Email')
        if full_name is None:
            raise TypeError('Users should have a Full name')

        user = self.model(email=self.normalize_email(email), full_name=full_name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, full_name, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(email, full_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    class Meta:
        db_table = "myjob_user"
    groups = None
    user_permissions = None

    username = None
    first_name = None
    last_name = None
    full_name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False, unique=True, db_index=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

from configs import variable_system as var_sys
from django.db import models
from django.contrib.auth.models import (AbstractUser, BaseUserManager)
from .base import AuthBaseModel


class UserManager(BaseUserManager):
    def create_user(self, email, full_name="name", password=None, **extra_fields):
        if email is None:
            raise ValueError('Users should have a email')
        if full_name is None:
            raise ValueError('Users should have a full name')

        user = self.model(email=self.normalize_email(email), full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        if password is None:
            raise ValueError('Super users should have a password')

        user = self.create_user_with_role_name(email, full_name, var_sys.ADMIN,
                                               password=password, is_superuser=True,
                                               is_staff=True, is_active=True)
        return user

    def create_user_with_role_name(self, email, full_name, role_name, password=None, **extra_fields):
        if role_name is None:
            raise ValueError("Role name is required!")
        user = self.create_user(email, full_name, password, **extra_fields)
        user.role_name = role_name
        user.save()

        return user


class User(AbstractUser, AuthBaseModel):
    groups = None
    user_permissions = None

    username = None
    first_name = None
    last_name = None
    date_joined = None
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True, db_index=True)
    avatar_url = models.URLField(max_length=300, default=var_sys.AVATAR_DEFAULT["USER_AVT"])
    phone = models.CharField(max_length=15, blank=True, null=True)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=var_sys.GENDER_CHOICES, null=True)
    email_notification_active = models.BooleanField(default=True)
    sms_notification_active = models.BooleanField(default=True)
    has_company = models.BooleanField(default=False)

    # ForeignKey
    role_name = models.CharField(max_length=10, choices=var_sys.ROLE_CHOICES,
                                 default=var_sys.JOB_SEEKER)

    class Meta:
        db_table = "myjob_authentication_user"

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

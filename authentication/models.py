from configs import variable_system as var_sys
from django.db import models
from django.contrib.auth.models import (AbstractUser, BaseUserManager)


class AuthBaseModel(models.Model):
    class Meta:
        abstract = True

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
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
                                               password=password,
                                               is_superuser=True,
                                               is_staff=True,
                                               is_active=True,
                                               is_verify_email=True)
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
    avatar_url = models.URLField(max_length=300, default=var_sys.AVATAR_DEFAULT["AVATAR"])
    avatar_public_id = models.CharField(max_length=300, null=True)
    email_notification_active = models.BooleanField(default=True)
    sms_notification_active = models.BooleanField(default=True)
    has_company = models.BooleanField(default=False)
    is_verify_email = models.BooleanField(default=False)

    # ForeignKey
    role_name = models.CharField(max_length=10, choices=var_sys.ROLE_CHOICES,
                                 default=var_sys.JOB_SEEKER)

    class Meta:
        db_table = "myjob_authentication_user"
        verbose_name_plural = "Users"

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]


class ForgotPasswordToken(AuthBaseModel):
    token = models.CharField(max_length=255, null=True)
    code = models.IntegerField(null=True)
    expired_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    platform = models.CharField(max_length=3, choices=var_sys.PLATFORM_CHOICES,
                                default="WEB")

    # ForeignKey
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forgot_password_tokens")

    class Meta:
        db_table = "myjob_authentication_forgot_password_token"

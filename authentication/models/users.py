from configs import variable_system as var_sys
from helpers import utils
from django.db import models
from django.contrib.auth.models import (AbstractUser, BaseUserManager)
from .base import AuthBaseModel
from .roles import Role


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
        role = Role.objects.filter(name__in=[var_sys.ADMIN])
        if not role.exists():
            raise TypeError(f"{var_sys.ADMIN} role does not exists!")
        user.roles.add(role.first())
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
    roles = models.ManyToManyField("Role", through="UserRole", related_name="users")

    class Meta:
        db_table = "myjob_authentication_user"

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]


class UserRole(AuthBaseModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey("Role", on_delete=models.CASCADE, related_name="user_roles")

    class Meta:
        db_table = 'myjob_authentication_user_role'

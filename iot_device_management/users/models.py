from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from . import managers


class User(AbstractBaseUser):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    update_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]
    objects = managers.UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        return f"{self.name}"

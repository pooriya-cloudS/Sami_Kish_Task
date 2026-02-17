from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("An email is required.")

        user = self.model(email=email)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, email, name):
        user = self.model(
            email=email,
            name=name,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user

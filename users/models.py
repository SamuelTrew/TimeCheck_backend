from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from utility.methods import generate_key
from utility.mixins import ModelDateMixin


# Should be a multiple of 4, or actual length may differ
USER_KEY_LENGTH = 16


def _generate_user_key():
    return generate_key(USER_KEY_LENGTH)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _assemble_user(self, email: str, name: str, mattcorp_id: str, **extra_fields) -> 'User':
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The email attribute must be given")
        if not name:
            raise ValueError("The name attribute must be given")
        if not mattcorp_id:
            raise ValueError("The mattcorp_id attribute must be given")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, mattcorp_id=mattcorp_id, **extra_fields)
        return user

    def create_user(self, email, name, mattcorp_id, **extra_fields) -> 'User':
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self._assemble_user(email, name, mattcorp_id, **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields) -> 'User':
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        user = self._assemble_user(email, password, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin, ModelDateMixin):
    id = models.CharField(
        "User ID",
        primary_key=True,
        max_length=USER_KEY_LENGTH,
        default=_generate_user_key,
        editable=False,
    )
    mattcorp_id = models.CharField(
        "MattCorp ID",
        max_length=100,
        unique=True,
    )
    name = models.CharField(
        "Name",
        max_length=150,
        blank=True,
    )
    email = models.EmailField(
        "Email address",
        error_messages={
            'unique': "A user with that email address already exists",
        },
    )
    email_verified = models.BooleanField(
        "Email verified",
        default=False,
    )
    is_staff = models.BooleanField(
        "Staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        "Active",
        default=True,
        help_text="Designates whether this user should be treated as active. "
                  "Unselect this instead of deleting accounts.",
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['name', 'email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.get_full_name()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the full name for the user.
        """
        return self.name.strip()

    def get_short_name(self):
        """
        Return the short name for the user.
        This is currently defined as the first word of the full name.
        """
        return self.get_full_name().split(None, 1)[0]

from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self,phone_number, password=None, **extra_fields):
        if not phone_number:
              raise ValueError("Phone number is required")

        user = self.model(phone_number=phone_number, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self,phone_number,password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(phone_number=phone_number,password=password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        max_length=255,
        unique=True,
        blank=True,
        null=True
    )

    

    phone_number = PhoneNumberField(
        unique=True
    )

    email_verified = models.BooleanField(
            default=False
        )
    phone_verified=models.BooleanField(
            default=False
        )

    is_staff = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    

    date_joined = models.DateTimeField(
        auto_now_add=True
    )

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    EMAIL_FIELD = "email"

    objects = UserManager()

   

    def __str__(self):
        return str(self.phone_number)



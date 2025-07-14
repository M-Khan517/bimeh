from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.core import validators
from random import randrange
import datetime
import pytz

# Create your models here.


class CustomeUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_field):

        if not phone:
            raise ValueError("شماره تلفن نمیتواند خالی باشد")

        phone = phone.strip()

        if self.model.objects.filter(phone=phone).exists():
            raise ValueError("شماره تلفن تکراری است")

        user = self.model(phone=phone, **extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_field):
        extra_field.setdefault("is_staff", True)
        extra_field.setdefault("is_superuser", True)
        extra_field.setdefault("is_active", True)

        return self.create_user(phone, password, **extra_field)


class User(AbstractBaseUser, PermissionsMixin):

    id = models.AutoField(primary_key=True)

    full_name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی")

    national_code = models.CharField(
        max_length=120, verbose_name="کدملی", db_index=True
    )
    phone = models.CharField(
        max_length=120,
        verbose_name="شماره تلفن",
        unique=True,
        validators=[
            validators.RegexValidator(
                r"^((\+98|0)9\d{9})$", message="شماره تلفن صحیح نمیباشد"
            )
        ],
    )

    is_active = models.BooleanField(default=False, verbose_name="حساب فعال / غیرفعال")
    is_staff = models.BooleanField(default=False, verbose_name="حساب کاربر")

    verify_code = models.CharField(
        max_length=6, verbose_name="کد تایید", blank=True, null=True, db_index=True
    )
    expire_verify_code = models.DateTimeField(
        verbose_name="انقضا کد تایید", blank=True, null=True
    )

    objects = CustomeUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def generate_verify_code(self):
        self.save()

    def save(self, *args, **kwargs):
        self.verify_code = randrange(100000, 999999)
        self.expire_verify_code = datetime.datetime.now(
            pytz.timezone("Asia/Tehran")
        ) + datetime.timedelta(minutes=2)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name}"

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"


class SubUser(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی")
    national_code = models.CharField(max_length=30, verbose_name="کدملی")
    manager = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="سرگروه",
        related_name="sub_users",
    )

    created_at = models.DateTimeField(
        verbose_name="تاریخ ساخت",
        editable=False,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.national_code}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = datetime.datetime.now()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "زیر مجموعه"
        verbose_name_plural = "زیر مجموعه ها"

        ordering = ["-created_at"]

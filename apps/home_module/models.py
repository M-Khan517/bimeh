import datetime
from django.db import models
from django.core import validators


class PilgrimageDestination(models.Model):
    name = models.CharField(max_length=220, verbose_name="نام مقصد زیارتی")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "مقصد"
        verbose_name_plural = "مقاصد زیارتی"


class CategoryFAQ(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="عنوان دسته بندی",
    )
    url_title = models.CharField(
        max_length=255,
        verbose_name="عنوان دسته بندی به انگلیسی",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "دسته بندی سوالات پرتکرار"
        verbose_name_plural = "دسته بندی های سوالات پرتکرار"


class QustionFAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name="عنوان سوال")
    response = models.TextField(verbose_name="پاسخ سوال")
    category = models.ForeignKey(
        CategoryFAQ,
        on_delete=models.CASCADE,
        verbose_name="دسته بندی",
        related_name="questions",
    )
    created_at = models.DateTimeField(
        verbose_name="تاریخ ایجاد", editable=False, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        self.created_at = datetime.datetime.now()
        return super().save(args, kwargs)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "سوال و جواب"
        verbose_name_plural = "سوالات و پاسخ های سوالات پرتکرار"


class Contact(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(
        max_length=120,
        verbose_name="شماره تلفن",
        validators=[
            validators.RegexValidator(
                r"^((\+98|0)9\d{9})$", message="شماره تلفن صحیح نمیباشد"
            )
        ],
    )
    message = models.TextField(verbose_name="پیام")
    created_at = models.DateTimeField(verbose_name="تاریخ ایجاد", null=True, blank=True)

    def save(self, *args, **kwargs):
        self.created_at = datetime.datetime.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = "درخواست تماس"
        verbose_name_plural = "درخواست های تماس"

        ordering = ["-created_at"]


class Gallery(models.Model):
    image = models.ImageField(verbose_name="تصویر", upload_to="Gallery")
    show_in_aboutUs = models.BooleanField(
        verbose_name="در درباره ما نمایش داده شود؟",
        default=True,
    )

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = "عکس"
        verbose_name_plural = "گالری"


class AboutUs(models.Model):
    text = models.TextField(verbose_name="درباره ما")

    class Meta:
        verbose_name = "درباره ما"
        verbose_name_plural = "درباره ما"

    def __str__(self):
        return self.text


class SettingSite(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="نام سایت", null=True, blank=True
    )
    logo = models.ImageField(
        verbose_name="لوگو", null=True, blank=True, upload_to="logo/"
    )
    phone = models.CharField(
        max_length=120, verbose_name="شماره تماس", null=True, blank=True
    )
    email = models.EmailField(verbose_name="ایمیل", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات های سایت"

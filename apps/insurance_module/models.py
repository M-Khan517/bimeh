from django.db import models
from apps.account_module.models import User, SubUser
from apps.home_module.models import PilgrimageDestination
from random import randrange, random, randint
from jalali_date.fields import datetime2jalali
from iranian_cities.fields import ProvinceField, CountyField
import datetime
from utils.sender.send_sms import send, send_with_pattern


class InsurancePrice(models.Model):
    all_value_day = models.SmallIntegerField(
        verbose_name="تعداد روز برای محاسبه تمام بها"
    )
    all_value_price = models.CharField(max_length=50, verbose_name="قیمت تمام بها")
    other_day_price = models.CharField(max_length=50, verbose_name="قیمت بقیه روز ها")

    def save(self, *args, **kwargs):
        if not self.pk and InsurancePrice.objects.exists():
            raise ValueError("از این مدل قبلا ساخته شده در صورت لزوم ویرایش کنید")
        return super().save(args, kwargs)

    def __str__(self):
        return f" نرخ روزهای تمام بها : {self.all_value_price} - روز های معمولی : {self.other_day_price}"

    class Meta:
        verbose_name = "نرخ بیمه"
        verbose_name_plural = "نرخ بیمه ها"


class Insurance(models.Model):

    STATUS = (
        ("0", "پرداخت نشده"),
        ("1", "درحال رسیدگی"),
        ("2", "رسیدگی شده"),
        ("3", "ردشده"),
    )

    PAY_STATUS = (("0", "پرداخت نشده"), ("1", "پرداخت شده"))

    code = models.CharField(
        max_length=9,
        verbose_name="کد رهگیری",
        db_index=True,
        editable=False,
    )

    manager = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="مدیر گروه",
        db_index=True,
        related_name="insurances",
    )
    subsets = models.ManyToManyField(
        SubUser,
        verbose_name="همراهان",
        null=True,
        blank=True,
        related_name="insurances",
    )
    destination = models.ForeignKey(
        to=PilgrimageDestination, on_delete=models.CASCADE, verbose_name="مقصد زیارتی"
    )

    insurance_maneger = models.BooleanField(
        verbose_name="مدیر گروه بیمه شود / نشود", default=False
    )

    origin_province = ProvinceField(verbose_name="استان مبدا")

    origin_county = CountyField(verbose_name="شهر مبدا", null=True, blank=True)

    insuranceprice = models.ForeignKey(
        to=InsurancePrice, on_delete=models.CASCADE, verbose_name="تعرفه محاسبه قیمت"
    )
    total_price = models.CharField(
        verbose_name="مبلغ قابل پرداخت", max_length=100, default=0
    )

    pay_status = models.CharField(
        max_length=220, verbose_name="وضعیت پرداخت", choices=PAY_STATUS, default=0
    )
    pay_date = models.DateTimeField(verbose_name="تاریخ پرداخت", null=True, blank=True)

    status = models.CharField(
        max_length=255, verbose_name="وضعیت درخواست", choices=STATUS, default=0
    )

    start_date = models.DateField(verbose_name="تاریخ شروع به حرکت")

    end_date = models.DateField(verbose_name="تاریخ بازگشت")

    created_at = models.DateTimeField(
        verbose_name="زمان ثبت درخواست", null=True, blank=True, editable=False
    )
    updated_at = models.DateTimeField(
        verbose_name="آخرین ویرایش درخواست", null=True, blank=True, editable=False
    )

    insurance_file = models.FileField(
        verbose_name="بیمه نامه", upload_to="insurance/", null=True, blank=True
    )

    def save(self, *args, **kwargs):

        if self.pk:
            self.updated_at = datetime.datetime.now()
        else:
            self.created_at = datetime.datetime.now()

            while True:
                temp = randint(1000, 999999999)
                if Insurance.objects.filter(code=temp).exists() == False:
                    self.code = temp
                    break
        if self.insurance_file:
            # send(
            #     self.manager.phone,
            #     f"مدیر کاروان عزیز فایلی برای بیمه نامه {self.code} بارگذاری شد به پنل بیمه زائر مراجعه کنید",
            # )

            send_with_pattern(344667, self.manager.phone, [self.code])

        return super().save(args, kwargs)

    def __str__(self):
        return f"{self.code}"

    class Meta:
        verbose_name = "بیمه"
        verbose_name_plural = "بیمه ها"

        ordering = ["-created_at"]


# class Compensation(models.Model):

#     STATUS = (("",""),("",""),("",""))

#     insurance = models.OneToOneField(
#         to=Insurance, on_delete=models.CASCADE, verbose_name="بیمه نامه"
#     )
#     subUsers = models.ManyToManyField(
#         to=SubUser, verbose_name="زائران آسیب دیده", null=True, blank=True
#     )
#     type_damage = models.CharField(
#         max_length=120,
#         verbose_name="نوع حادثه",
#         choices=(("فوت", "death"), ("صدمات جسمانی", "dameged")),
#     )
#     description = models.TextField(verbose_name="شرح حادثه")
#     damage_date = models.DateField(verbose_name="تاریخ وقوع حادثه")
#     address = models.TextField(verbose_name="نشانی کامل محل وقوع حادثه")
#     hospital = models.CharField(
#         max_length=255,
#         verbose_name="مرکز درمانی مورد نظر جهت معالجه یا مداوا بلافاصله بعد از بروز حادثه",
#     )

#     status =

#     created_at = models.DateTimeField(verbose_name="")

#     def __str__(self):
#         return f"{self.insurance.code} - {self.get_type_damage_display}"

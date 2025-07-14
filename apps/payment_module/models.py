from django.db import models

from apps.insurance_module.models import Insurance


class PaymentLog(models.Model):
    insurance = models.OneToOneField(
        Insurance, on_delete=models.CASCADE, verbose_name="بیمه"
    )
    ref_id = models.CharField(max_length=250, verbose_name="کد پرداخت")
    pay_date = models.DateTimeField(verbose_name="تاریخ پرداخت")
    price = models.CharField(max_length=250, verbose_name="مبلغ")

    def __str__(self):
        return self.ref_id

    class Meta:
        verbose_name = "گزارش"
        verbose_name_plural = "گزارش ها"
        ordering = ["-pay_date"]

from django.contrib import admin
from .models import PaymentLog
from jalali_date.admin import ModelAdminJalaliMixin

# Register your models here.


@admin.register(PaymentLog)
class PaymentLogAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ["ref_id", "price", "pay_date"]
    search_fields = ["ref_id"]

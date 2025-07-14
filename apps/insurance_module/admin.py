from django.contrib import admin
from django.urls import reverse
from .models import InsurancePrice, Insurance
from jalali_date.admin import ModelAdminJalaliMixin
from iranian_cities.admin import IranianCitiesAdmin
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html

# Register your models here.


@admin.register(InsurancePrice)
class InsurancePriceAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if InsurancePrice.objects.exists():
            return False
        return True
        # return super().has_add_permission(request)


@admin.register(Insurance)
class InsuranceAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):

    list_display = [
        "code",
        "manager",
        "insurance_maneger",
        "total_price",
        "created_at",
        "status",
        "export_button",
    ]

    search_fields = ["code", "manager__national_code"]

    sortable_by = [
        "show_created_at",
        "show_updated_at",
    ]

    list_filter = ["status"]

    def export_button(self, obj):
        url = reverse("export", args=[obj.id])
        return format_html("<a class='btn btn-success' href='{}'>.xls</a>", url)

    export_button.short_description = "خروجی"

    class Media:
        js = ["js/jquery-3.7.1.slim.min.js", "js/insurance_admin.js"]

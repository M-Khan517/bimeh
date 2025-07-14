from django.contrib import admin
from .models import User, SubUser
from import_export.admin import ImportExportModelAdmin
from jalali_date.admin import ModelAdminJalaliMixin


# Register your models here.
@admin.register(User)
class UserModelAdmin(ImportExportModelAdmin):
    search_fields = ["national_code", "phone", "full_name"]


@admin.register(SubUser)
class SubUserModelAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    search_fields = ["national_code", "full_name"]
    list_display = ["full_name", "national_code", "created_at"]

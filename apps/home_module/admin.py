from django.contrib import admin
from .models import (
    PilgrimageDestination,
    CategoryFAQ,
    QustionFAQ,
    SettingSite,
    AboutUs,
    Gallery,
    Contact,
)

# Register your models here.


@admin.register(SettingSite)
class SiteSettingModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if SettingSite.objects.exists():
            return False
        return True


@admin.register(AboutUs)
class AboutUsModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if AboutUs.objects.exists():
            return False

        return True


admin.site.register(PilgrimageDestination)
admin.site.register(CategoryFAQ)
admin.site.register(QustionFAQ)
admin.site.register(Gallery)
admin.site.register(Contact)

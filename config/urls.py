from django.contrib import admin
from django.urls import include, path
from web_project.views import SystemView
from django.conf import settings
from django.conf.urls.static import static

# ستایشگران نور

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.home_module.urls")),
    path("auth/", include("apps.account_module.urls")),
    path("insurance/", include("apps.insurance_module.urls")),
    path("py/", include("apps.payment_module.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = SystemView.as_view(template_name="pages_misc_error.html", status=404)
handler403 = SystemView.as_view(
    template_name="pages_misc_not_authorized.html", status=403
)
handler400 = SystemView.as_view(template_name="pages_misc_error.html", status=400)
handler500 = SystemView.as_view(template_name="pages_misc_error.html", status=500)

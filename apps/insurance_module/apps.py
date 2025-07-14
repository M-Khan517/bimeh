from django.apps import AppConfig


class InsuranceModuleConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.insurance_module"
    verbose_name = "بیمه"

    def ready(self):
        import apps.insurance_module.signals

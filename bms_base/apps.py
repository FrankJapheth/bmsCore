from django.apps import AppConfig


class BmsBaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bms_base'
    verbose_name = "Business Management System Base"

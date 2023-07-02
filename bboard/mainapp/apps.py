from django.apps import AppConfig
import django.dispatch

class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainapp'
    verbose_name = 'Объявления'

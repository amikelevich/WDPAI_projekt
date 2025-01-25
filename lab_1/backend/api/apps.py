from django.apps import AppConfig

#konfiguracja aplikacji, ustawia typ na klucz główny bigautofield oraz nazwę aplikacji
class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

from django.apps import AppConfig


class TestDjangoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_django'

    def ready(self):
        import test_django.signal


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        import test_django.signal

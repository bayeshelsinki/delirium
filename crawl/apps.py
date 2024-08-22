# crawl/apps.py
from django.apps import AppConfig

class CrawlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crawl'

    def ready(self):
        import crawl.signals  # Import the signals module to ensure it gets registered

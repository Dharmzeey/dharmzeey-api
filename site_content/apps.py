from django.apps import AppConfig


class SiteContentConfig(AppConfig):
    name = 'site_content'

    def ready(self):
        from core.netlify import watch
        watch(self.get_model('SiteContent'))

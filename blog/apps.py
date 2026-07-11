from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        from core.netlify import watch
        watch(self.get_model('Tag'), self.get_model('BlogPost'))

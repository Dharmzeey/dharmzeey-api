from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    name = 'projects'

    def ready(self):
        from core.netlify import watch
        watch(self.get_model('Project'))

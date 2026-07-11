from django.apps import AppConfig


class SkillsConfig(AppConfig):
    name = 'skills'

    def ready(self):
        from core.netlify import watch
        watch(self.get_model('SkillCategory'), self.get_model('Skill'))

from django.apps import AppConfig


class LearnquestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'learnquest'
    
    def ready(self):
        import learnquest.signals  




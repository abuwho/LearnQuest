from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """
    Configuration class for the authentication app.
    
    Attributes:
        default_auto_field (str): The default auto-generated field for models (set to 'django.db.models.BigAutoField').
        name (str): The name of the authentication app.
    
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

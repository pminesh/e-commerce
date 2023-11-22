from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # name = 'cart'
    name = __name__.rpartition('.')[0]

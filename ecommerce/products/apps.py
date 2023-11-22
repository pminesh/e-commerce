from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # name = 'products'
    name = __name__.rpartition('.')[0]

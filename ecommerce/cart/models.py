from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from ecommerce.cart.managers import CartManager
from ecommerce.products.models import Product


class Cart(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="users")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products")
    quantity = models.PositiveSmallIntegerField(_("product quantity"), default=1)

    objects = CartManager()

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _("Carts")

    def __str__(self):
        return f"{self.product}"

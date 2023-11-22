from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model
from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel
from ecommerce.custom_auth.models import Address
from ecommerce.products.models import Product
from hashid_field import HashidAutoField

User = get_user_model()


class Order(TimeStampedModel):
    STATUS = Choices(
        ('pending', 'Pending'), #pending, accepted, rejected, cancle, shipped, on the way, delevered
        ('delevered', 'Delevered'),
        ('reject', 'Reject')
    )

    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='user_address')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_detail')
    order_number = models.CharField(max_length=128)
    # order_number = HashidAutoField()
    total = models.FloatField(default=0.0)
    ordered_date = models.DateTimeField(default=timezone.now)
    payment_type = models.CharField(max_length=16)
    status = models.CharField(max_length=16, choices=STATUS, default=STATUS.pending)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'{self.user.username}'


class OrderDetail(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='customer_order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_detail')
    quantity = models.PositiveSmallIntegerField()
    price = models.FloatField()

    class Meta:
        verbose_name = _('OrderDetail')
        verbose_name_plural = _('OrderDetails')

    def __str__(self):
        return f'{self.order}'

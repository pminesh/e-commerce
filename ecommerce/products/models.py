from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from ecommerce.category.models import Category
from ecommerce.utils.utils import get_product_photo_path


class Product(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=256, unique=True,
                            error_messages={'unique': _('A product with that name already exists.')})
    price = models.FloatField(_('selling price'))
    discount = models.FloatField(_('discount percentage(%)'), null=True, blank=True)
    slug = models.SlugField(_('slug'), max_length=256, blank=True, null=True)
    description = models.TextField(_('description'), null=True, blank=True)
    stocks = models.IntegerField(_('number of stocks'), null=True, blank=True, default=0)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(
        upload_to=get_product_photo_path,
        height_field='height',
        width_field='width',
        null=True,
        blank=True
    )
    height = models.PositiveSmallIntegerField(blank=True, null=True)
    width = models.PositiveSmallIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.image and (not self.width and self.height):
            self.width = self.image.width
            self.height = self.image.height
        super().save(*args, **kwargs)

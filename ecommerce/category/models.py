from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(_('name'), max_length=150, unique=True,
                            error_messages={'unique': _('A category with that name already exists.')})
    slug = models.SlugField(_('slug'), max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

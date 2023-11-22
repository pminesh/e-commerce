from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from ecommerce.utils.models import GenericBase
from ecommerce.utils.utils import get_document_path


class Attachment(GenericBase):
    file = models.FileField(upload_to=get_document_path, max_length=500)
    added_at = models.DateTimeField(_("Created at"), editable=False, default=timezone.now)

    class Meta:
        verbose_name = _("file")
        verbose_name_plural = _("Files")

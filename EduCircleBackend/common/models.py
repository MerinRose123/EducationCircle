import datetime
import os
import random
import uuid

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType


class BaseModel(models.Model):
    # Unique ID as the Primary Key instead of the default Integer Primary Key
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False,
                           verbose_name='unique id')

    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='creation date')
    modified_at = models.DateTimeField(db_index=True, auto_now=True, blank=True, null=True,
                                       verbose_name='last modified')


    description = models.CharField(_('Description'), max_length=1500, blank=True,null=True, default='')

    class Meta:
        # To prevent it's migration, we set it as abstract
        abstract = True

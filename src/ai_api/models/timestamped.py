__author__ = "root"
__date__ = "09/03/2022, 02:00 PM"

from django.db import models
from django.utils import timezone

from ai_api.models.customtypes import SimpleDateTimeField


class AutoTimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SimpleTimeStampedModel(models.Model):
    created_at = SimpleDateTimeField(default=timezone.now)
    updated_at = SimpleDateTimeField(auto_now=True)

    class Meta:
        abstract = True

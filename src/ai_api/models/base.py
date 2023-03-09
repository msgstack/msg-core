__author__ = "root"
__date__ = "28/02/2022, 04:00 PM"

import uuid

from django.db import models
from dirtyfields import DirtyFieldsMixin

from aicore.models.manager import BaseManager
from ai_api.models.soft_delete import SoftDeleteModel
from ai_api.models.timestamped import AutoTimeStampedModel, SimpleTimeStampedModel


class BaseQueryModel(models.Model):
    @classmethod
    def get_default_allowed_fields(cls):
        return [f.name for f in cls._meta.get_fields(include_parents=False)]

    @classmethod
    def set_updatable_fields_values(cls, obj, **kwargs):
        allowed_fields = obj.get_default_allowed_fields()
        for k, v in kwargs.items():
            if k in allowed_fields:
                setattr(obj, k, v)
        return obj

    @classmethod
    def get_updatable_fields(cls, **kwargs):
        return getattr(cls._meta, "updatable_fields", []) or cls.get_default_allowed_fields()

    @classmethod
    def get_creatable_fields(cls):
        return getattr(cls._meta, "creatable_fields", [])

    @classmethod
    def is_allow_set_creatable_field(cls, key):
        return True

    @classmethod
    def upsert(cls, model, data, allow_empty_value=True, **kwargs):
        is_update = bool(model.pk)
        updatable_fields = list(cls.get_updatable_fields(**kwargs))
        allowed_fields = cls.get_default_allowed_fields()
        if "updated_at" in allowed_fields:
            updatable_fields.append("updated_at")
        if "updated_by" in allowed_fields:
            updatable_fields.append("updated_by")

        for key, value in data.items():
            if hasattr(model, key):
                if is_update:
                    has_value = bool(value)
                    allowed_set_field = (key in updatable_fields) and (allow_empty_value or has_value)
                else:
                    allowed_set_field = cls.is_allow_set_creatable_field(key)

                if allowed_set_field:
                    setattr(model, key, value)

        if is_update:
            model.save(updatable_fields=updatable_fields)
        else:
            model.save()


class UUIDModel(models.Model, DirtyFieldsMixin):
    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)
    objects = BaseManager()

    class Meta:
        abstract = True

    @classmethod
    def get_by_uuid(cls, uuid=None):
        return cls.objects.get(uuid=uuid)


class UUIDAutoTimeStampedModel(AutoTimeStampedModel, UUIDModel):
    class Meta:
        abstract = True


class UUIDSimpleTimeStampedModel(SimpleTimeStampedModel, UUIDModel):
    class Meta:
        abstract = True


class UUIDSoftDeleteModel(SoftDeleteModel, UUIDModel):
    class Meta:
        abstract = True

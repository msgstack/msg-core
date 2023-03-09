__author__ = "root"
__date__ = "09/03/2022, 02:30 PM"

from django.utils import timezone
from django.db import models

from ai_api.utils import utils
from aicore.models.queryset import BaseQuerySet, bulk_update
from aicore.models.manager import BaseManager


def set_delete_attributes(obj, deleted_by):
    obj.is_deleted = True
    obj.delete_at = timezone.now()
    obj.delete_by = deleted_by
    update_is_active = isinstance(getattr(obj, "is_active", None), bool)
    if update_is_active:
        obj.is_active = False
    return obj, update_is_active


class SoftDeleteQuerySet(BaseQuerySet):
    def delete(self):
        from ai_api.authentication import get_current_user

        current_user = get_current_user()
        deleted_by = utils.safe_int(getattr(current_user, "id", 0))
        update_fields = ["is_deleted", "deleted_by", "deleted_at"]
        update_is_active = False

        for obj in self:
            obj, update_is_active = set_delete_attributes(obj, deleted_by=deleted_by)
        if update_is_active:
            update_fields.append("is_active")
        bulk_update(self, update_fields=update_fields)


class SoftDeleteManager(BaseManager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def include_deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db)


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(default=None, null=True)
    deleted_by = models.PositiveIntegerField(default=0)

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def delete(self, request_user_id=0):
        obj, _ = set_delete_attributes(self, deleted_by=request_user_id)
        obj.save()

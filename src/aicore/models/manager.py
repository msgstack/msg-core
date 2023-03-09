__author__ = "root"
__date__ = "09/03/2022, 02:00 PM"

from typing import Any, Type, TypeVar

from django.db.models import Manager, Model
from django.db.models.signals import class_prepared, post_save

from aicore.models.queryset import BaseQuerySet

M = TypeVar("M", bound=Model)


class BaseManager(Manager):
    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db)

    def translate(self, *args, **kwargs):
        if hasattr(self, "translate"):
            return super().all().translate(*args, **kwargs)
        return self


class BaseSocketManager(BaseManager):
    def contribute_to_class(self, model: M, name: str) -> None:
        super().contribute_to_class(model, name)
        class_prepared.connect(self.__class_prepared, sender=model)

    def __class_prepared(self, sender: Any, **kwargs: Any) -> None:
        post_save.connect(
            self.post_save, sender=sender, weak=False, dispatch_uid=f"{sender._meta.model_name}_post_save_signal"
        )

    def post_save(self, instance: M, **kwargs: Any) -> None:
        pass

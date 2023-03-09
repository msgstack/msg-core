__author__ = "root"
__date__ = "09/03/2022, 02:00 PM"

from contextlib import suppress
from bulk_update.helper import bulk_update as dj_bulk_update
from django.db.models.query import QuerySet
from django.db.models.signals import post_save, pre_save
from django.db.utils import DEFAULT_DB_ALIAS


def bulk_update(objs, **kwargs):
    exclude_fields = kwargs.get("exclude_fields", [])
    pre_save_signal = kwargs.get("trigger_signal", False)
    post_save_signal = kwargs.get("post_save_signal", False)

    if objs:
        _model = objs[0]
        if pre_save_signal:
            for obj in objs:
                pre_save.send(obj.__class__, instance=obj, raw=None)

        from ai_api.utils import utils
        update_fields = utils.list_diff(exclude_fields, kwargs.get("update_fields", []))

        with suppress(Exception):
            getattr(_model, "uuid")
            exclude_fields.append("uuid")

        result = dj_bulk_update(
            objs,
            meta=kwargs.get("meta", None),
            update_fields=update_fields,
            exclude_fields=exclude_fields,
            using=kwargs.get("using", DEFAULT_DB_ALIAS),
            batch_size=kwargs.get("batch_size", None),
            pk_field=kwargs.get("pk_field", "pk")
        )

        if post_save_signal:
            for obj in objs:
                post_save.send(obj.__class__, instance=obj, created=True, raw=None)

        return result
    return None


class MultilingualQuerySet(QuerySet):
    pass


class BaseQuerySet(MultilingualQuerySet):
    pass

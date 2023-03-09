__author__ = "root"
__date__ = "09/03/2022, 02:00 PM"

try:
    from threading import local
except ImportError:
    # noinspection PyUnresolvedReferences
    from django.utils._threading_local import local

ai_global = local()

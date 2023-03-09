__author__ = "root"
__date__ = "09/03/2022, 02:30 PM"

from contextlib import contextmanager, suppress


class utils:
    @staticmethod
    def safe_int(val, default=0):
        with suppress(Exception):
            return int(val)
        return default

    @staticmethod
    def list_diff(base_list, list_has_diff):
        return list(set(list_has_diff) - set(base_list))

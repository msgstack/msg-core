__author__ = "root"
__date__ = "09/03/2022, 02:30 PM"

from ai_api import ai_global


def get_current_request():
    return getattr(ai_global, "request", None)


def get_current_user():
    request = get_current_request()
    if request:
        return getattr(request, "user", None)

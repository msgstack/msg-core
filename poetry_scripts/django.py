import string
from os import environ
from os import path as ospath
from os import system as ossyscall

from sys import argv
from sys import path as syspath
from pathlib import Path

import django
from django.conf import settings
from django.core.management import call_command

PROJECT_ROOT = Path(__file__).resolve().parent.parent / "src"
MANAGE_PY = PROJECT_ROOT / "manage.py"


def noop(*args, **kwargs):
    pass  # noqa


def boot_django():
    syspath.append(str(PROJECT_ROOT))
    environ.setdefault("DJANGO_SETTINGS_MODULE", "aicore.settings")
    django.setup()


def __getattr__(cmd: string):
    args = argv[1:]
    boot_django()
    if cmd.endswith("server"):
        if not any(":" in arg for arg in args):
            args.append(f"0.0.0.0:{settings.API_PORT}")
        ossyscall(f"python {MANAGE_PY} {cmd} {' '.join(args)}")
    else:
        call_command(cmd, args)
    return noop

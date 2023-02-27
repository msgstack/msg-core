import environ

from pathlib import Path
from split_settings.tools import optional, include

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

env_file = BASE_DIR / "config.env"
if env_file.exists():
    environ.Env.read_env(str(env_file))

APP_ENVIRONMENT = env.str("APP_ENVIRONMENT", default="production")

_base_settings = (
    "configs/[!_]*.py",
    f"environments/{APP_ENVIRONMENT}.py",
    optional("environments/optional.py")
)

include(*_base_settings)

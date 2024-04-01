import os


ADMINS = set(int(x) for x in os.environ.get("ADMINS", "").split())
DATABASE = os.environ.get("DATABASE_URL")
DEFAULT_LANGUAGE = os.environ.get("DEFAULT_LANGUAGE", "en")

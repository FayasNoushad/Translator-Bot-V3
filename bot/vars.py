import os


ADMINS = set(int(x) for x in os.environ.get("ADMINS", "").split())
DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "Translator-Bot")
DEFAULT_LANGUAGE = os.environ.get("DEFAULT_LANGUAGE", "en")

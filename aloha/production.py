from aloha.settings import *

DEBUG=False
TEMPLATE_DEBUG=DEBUG


DATABASES["default"]["ENGINE"] = 'django.db.backends.mysql'
DATABASES["default"]["NAME"] = ''
DATABASES["default"]["USER"] = ''

from aloha.local import DATABASE_PASSWORD
# Imports DATABASE_PASSWORD from testapp/local.py that is not part of git repo
DATABASES["default"]["PASSWORD"] = DATABASE_PASSWORD

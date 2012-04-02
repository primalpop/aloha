from aloha.settings import *

DEBUG=False
TEMPLATE_DEBUG=DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'jamallotment',                      # Or path to database file if using sqlite3.
        'USER': 'jam_user',                      # Not used with sqlite3.
        'PASSWORD': 'Jam@2012Fossee',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

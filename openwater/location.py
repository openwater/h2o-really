#!/usr/bin/env python
# -*- coding: utf-8 -*-

DATABASES = {
    'default': {
        'ENGINE': 'django_hstore.backends.postgis', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'openwater',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'spike',
#        'PASSWORD': '',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
#        'PORT': '',                      # Set to empty string for default.
    }
}

"""
WSGI config for machinelol project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('C:/Users/Vichoko/Documents/GitHub/final/Django')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "machinelol.settings")

application = get_wsgi_application()

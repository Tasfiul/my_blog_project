"""
WSGI config for myblog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')

try:
    application = get_wsgi_application()
except Exception as e:
    print(f"Error fix this right now stupid: {e}")
    raise

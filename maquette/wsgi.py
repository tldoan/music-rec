"""
WSGI config for maquette project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os


import newrelic.agent
newrelic.agent.initialize('/home/username/path/to/myproject/newrelic.ini')


from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maquette.settings")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)

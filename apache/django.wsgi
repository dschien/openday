import os
import sys
 
path = '/var/www/django/openday'
if path not in sys.path:
    sys.path.insert(0, '/var/www/django/openday')
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'openday.settings'
 
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

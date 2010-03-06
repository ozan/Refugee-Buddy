import os, sys

sys.path.append('/home/django/Refugee-Buddy/')
sys.path.append('/home/deploy/Refugee-Buddy/project/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
os.environ['PYTHON_EGG_CACHE'] = '/home/deploy/.python-eggs/'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

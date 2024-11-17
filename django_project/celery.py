from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Assurez-vous que les paramètres Django sont chargés correctement
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

app = Celery('django_project')

# Chargez les configurations de Celery à partir de Django settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Découvrez automatiquement les tâches Celery dans les applications Django
app.autodiscover_tasks()

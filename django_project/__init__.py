from __future__ import absolute_import, unicode_literals

# Cela garantira que Celery est toujours importé lorsque Django démarre
from .celery import app as celery_app

__all__ = ('celery_app',)

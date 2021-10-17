from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import FileSystemStorage


PROTECED_MEDIA = getattr(settings, 'PROTECTED_MEDIA', None)

if PROTECED_MEDIA == None:
    raise ImproperlyConfigured('PROTECTED_MEDIA is not set in settings.py')


class ProtectedStorage(FileSystemStorage):
    location = PROTECED_MEDIA   # MEDIA_ROOT
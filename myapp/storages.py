from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import FileSystemStorage



PROTECTED_MEDIA = getattr(settings, 'PROTECTED_MEDIA', None)

if PROTECTED_MEDIA == None:
    raise ImproperlyConfigured('Protected media is not set in the settings')


# default class for storing
class ProtectedStorage(FileSystemStorage):
    location = PROTECTED_MEDIA  # MEDIA_ROOT
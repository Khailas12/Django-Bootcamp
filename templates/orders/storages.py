from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import FileSystemStorage


PROTECTED_MEDIA = getattr(settings, 'PROTECTED_MEDIA', None)    # it could be stored in azure, google cloud etc

if PROTECTED_MEDIA == None:
    raise ImproperlyConfigured('PROTECTED_MEDIA is not set in settings')


class ProtectedStorage(FileSystemStorage):
    location = PROTECTED_MEDIA  # MEDIA_ROOT
    
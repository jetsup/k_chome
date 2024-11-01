from django.conf import settings
from django.http import HttpRequest
import uuid

def get_site_url(request: HttpRequest) -> str:
    if settings.DEBUG:
        return str(request.build_absolute_uri('/')[:-1])
    else:
        return str(settings.SITE_URL)

def generate_short_uuid() -> str:
    uuid_obj = uuid.uuid4()
    short_uuid = uuid_obj.hex[:16]  # Take the first 16 hexadecimal characters
    return short_uuid

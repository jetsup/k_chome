from django.conf import settings
from django.http import HttpRequest

def settings_context(request: HttpRequest) -> dict:
  return {'settings': settings}

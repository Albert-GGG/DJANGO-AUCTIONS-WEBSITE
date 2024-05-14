import zoneinfo
from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Enter your own timezone
        tzname = "America/Mexico_City"
        timezone.activate(zoneinfo.ZoneInfo(tzname))
    
        return self.get_response(request)
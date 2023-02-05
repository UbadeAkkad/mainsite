from .models import AccessLog
from django.utils import timezone


class AccessLogsMiddleware(object):

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):

        access_logs_data = dict()

        access_logs_data["path"] = request.path
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        access_logs_data["ip_address"] = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
        access_logs_data["method"] = request.method
        access_logs_data["referrer"] = request.META.get('HTTP_REFERER',None)
        access_logs_data["timestamp"] = timezone.now()
        if request.user.is_authenticated:
            access_logs_data["user"] = request.user.get_username()
        else:
            access_logs_data["user"] = "Anonymous"

        try:
            if access_logs_data["path"].split("/")[1] != "notadmin":
                AccessLog(**access_logs_data).save()
        except Exception as e:
            pass

        response = self.get_response(request)
        return response
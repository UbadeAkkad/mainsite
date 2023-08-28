from .models import AccessLog
from django.utils import timezone
import json
import requests

logging_block = ["notadmin","favicon.ico"]          #disable logging for this direct pathes

class AccessLogsMiddleware(object):

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):

        access_logs_data = dict()

        access_logs_data["path"] = request.path
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        access_logs_data["ip_address"] = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
        access_logs_data["method"] = request.method
        access_logs_data["params"] = request.META['QUERY_STRING']
        access_logs_data["referrer"] = request.META.get('HTTP_REFERER',None)
        access_logs_data["timestamp"] = timezone.now()
        if request.user.is_authenticated:
            access_logs_data["user"] = request.user.get_username()
        else:
            access_logs_data["user"] = "Anonymous"

        if AccessLog.objects.filter(ip_address = access_logs_data["ip_address"]).exists() and AccessLog.objects.filter(ip_address = access_logs_data["ip_address"])[0].location != " / ":
            try:
                other_access = AccessLog.objects.filter(ip_address = access_logs_data["ip_address"])[0]
                access_logs_data["location"] = other_access.location
                access_logs_data["isp"] = other_access.isp
            except:
                pass
        else:
            try:
                ip_api = "http://ip-api.com/json/{ip}".format(ip=access_logs_data["ip_address"])
                data = json.loads(requests.get(ip_api).content)
                access_logs_data["location"] = data["country"]+ " / " + data["city"]
                access_logs_data["isp"] = data["isp"]
            except:
                pass

        try:
            main_path = access_logs_data["path"].split("/")[1]
            if main_path not in logging_block:
                AccessLog(**access_logs_data).save()
        except Exception as e:
            pass

        response = self.get_response(request)
        return response
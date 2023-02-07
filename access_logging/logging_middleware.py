from .models import AccessLog
from django.utils import timezone
import json
import requests
from decouple import config


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

        if AccessLog.objects.filter(ip_address = access_logs_data["ip_address"]).exists() and AccessLog.objects.filter(ip_address = access_logs_data["ip_address"])[0].location != " / ":
            try:
                other_access = AccessLog.objects.filter(ip_address = access_logs_data["ip_address"])[0]
                access_logs_data["location"] = other_access.location
                access_logs_data["isp"] = other_access.isp
            except:
                pass
        else:
            try:
                ip_api = "https://api.ipgeolocation.io/ipgeo?apiKey={key}&ip={ip}".format(key=config("API_IP_TOKEN"),ip=access_logs_data["ip_address"])
                data = json.loads(requests.get(ip_api).content)
                access_logs_data["location"] = data["country_name"] + " / " + data["city"]
                access_logs_data["isp"] = data["organization"]
            except:
                pass

        try:
            if access_logs_data["path"].split("/")[1] != "notadmin":
                AccessLog(**access_logs_data).save()
        except Exception as e:
            pass

        response = self.get_response(request)
        return response
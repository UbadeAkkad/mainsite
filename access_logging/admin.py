from django.contrib import admin
from .models import AccessLog, AccessLogAdmin

admin.site.register(AccessLog, AccessLogAdmin, list_display = ["timestamp", "ip_address","path", "params","method", "location", "isp", "referrer", "user"])
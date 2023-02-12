from django.db import models
from django.contrib import admin
from django.http import HttpResponse
import csv
from datetime import datetime

class AccessLog(models.Model):
    sys_id = models.AutoField(primary_key=True, null=False, blank=True)
    path = models.CharField(max_length=1024, null=False, blank=True)
    method = models.CharField(max_length=8, null=False, blank=True)
    ip_address = models.CharField(max_length=45, null=False, blank=True)
    referrer = models.CharField(max_length=512, null=True, blank=True)
    timestamp = models.DateTimeField(null=False, blank=True)
    user = models.CharField(max_length=200, default="Anonymous")
    location = models.CharField(max_length=200, default=" / ")
    isp = models.CharField(max_length=200, default="Unknown")

    class Meta:
        db_table = "access_logs"

class AccessLogAdmin(admin.ModelAdmin):
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format("Access_log_" + datetime.now().strftime("%m-%d-%Y_%H-%M-%S"))
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"
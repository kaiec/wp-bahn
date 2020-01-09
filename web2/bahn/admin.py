from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Segment)
admin.site.register(models.Verbindung)
admin.site.register(models.Fahrt)

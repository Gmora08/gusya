from django.contrib import admin
from . import models

admin.site.register(models.WaitingList)
admin.site.register(models.Payment)

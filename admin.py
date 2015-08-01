from django.contrib import admin
from .models import Schedule, Event, Location

from modeltranslation.admin import TranslationAdmin

class EventAdmin(TranslationAdmin):
    list_per_page = 10000
    list_display = ('name', 'starttime', 'endtime')

    def starttime(self, obj):
        return obj.time.strftime("%A %d. %B %Y %H:%M")

    def endtime(self, obj):
        if (obj.time.strftime("%d") == obj.end_time.strftime("%d")):
            return obj.end_time.strftime("%H:%M")
        else:
            return obj.end_time.strftime("%A %H:%M")


class LocationAdmin(TranslationAdmin):
    pass

admin.site.register(Schedule)
admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)

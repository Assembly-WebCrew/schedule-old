from modeltranslation.translator import translator, TranslationOptions
from .models import Event, Location


class LocationTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


class EventTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

translator.register(Location, LocationTranslationOptions)
translator.register(Event, EventTranslationOptions)

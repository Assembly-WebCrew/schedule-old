from django.http import HttpResponse
import dateutil.tz
import json
import re
from schedule.models import Schedule, Event, Location
import string


def clean_json_dictionary_value(dictionary, key):
    if key not in dictionary:
        return
    if not dictionary[key]:
        return
    dictionary[key] = dictionary[key].replace("\r", "")
    dictionary[key] = dictionary[key].strip()

def encode_export_date(datetimeobj, tzlocal):
    if not datetimeobj:
        return None
    return datetimeobj.replace(tzinfo=tzlocal).strftime("%Y-%m-%dT%H:%M%z")

def dict_add_if_value_nonzero(dictionary, key, value):
    if value:
        dictionary[key] = value

def events_to_json(request, schedule_key):
    try:
        schedule = Schedule.objects.get(key=schedule_key)
    except Schedule.DoesNotExist:
        return {'error': 'schedule does not exists'}

    result = {}

    tzlocal = dateutil.tz.tzlocal()
    location_objects = Location.objects.filter(schedule=schedule)
    locations = {}
    for location in location_objects:
        location_data = {'name': location.name}
        dict_add_if_value_nonzero(location_data, 'name_fi', location.name)
        dict_add_if_value_nonzero(location_data, 'url', location.url)
        dict_add_if_value_nonzero(
            location_data, 'description', location.description)
        dict_add_if_value_nonzero(
            location_data, 'description_fi', location.description)
        locations[location.key] = location_data
    result['locations'] = locations

    events = []
    event_objects = Event.objects.filter(
        location__schedule=schedule, hidden=False).order_by("time", "order")
    for event in event_objects:
        event_key = "%s-%s" % (schedule_key, event.key)
        event_data = {
            'key': event_key,
            'name': event.name,
            'start_time': encode_export_date(event.time, tzlocal)
            }
        dict_add_if_value_nonzero(event_data, 'name_fi', event.name)
        dict_add_if_value_nonzero(
            event_data,
            'original_start_time',
            encode_export_date(event.original_time, tzlocal))
        dict_add_if_value_nonzero(
            event_data, 'end_time', encode_export_date(event.end_time, tzlocal))
        dict_add_if_value_nonzero(event_data, 'url', event.url)
        dict_add_if_value_nonzero(
            event_data, 'description', event.description)
        clean_json_dictionary_value(event_data, 'description')
        if event.location:
            dict_add_if_value_nonzero(
                event_data, 'location_key', event.location.key)
        dict_add_if_value_nonzero(
            event_data, 'description_fi', event.description)
        clean_json_dictionary_value(event_data, 'description_fi')
        flags = []
        if event.canceled:
            flags.append("canceled")
        if event.flags:
            flags.extend(event.flags.split(","))
        flags = [flag.strip() for flag in flags]
        flags = [flag for flag in flags if flag]
        event_data['flags'] = flags
        categories = [
            category.strip() for category in event.categories.split(",")]
        categories = [category for category in categories if category]
        event_data['categories'] = categories
        events.append(event_data)
    result['events'] = events

    data = json.dumps(result)
    return HttpResponse(data, content_type="application/json")


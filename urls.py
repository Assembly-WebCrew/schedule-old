from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<schedule_key>[\w-]+)/json/$', views.events_to_json),
]

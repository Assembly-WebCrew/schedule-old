from django.db import models
from datetime import timedelta, datetime


class Schedule(models.Model):
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    key = models.CharField(max_length=255, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    schedule = models.ForeignKey(Schedule)

    def __str__(self):
        return self.name


class Event(models.Model):
    key = models.CharField(max_length=255, blank=False, null=False)
    name = models.CharField(max_length=255)
    time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    original_time = models.DateTimeField()
    url = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    hidden = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    flags = models.CharField(max_length=255, blank=True)
    """ ^
    major: major events get more visibility than non-major
    asmtv: event is shown on AssemblyTV
    bigscreen: event is shown on the big screen
    onsite: event enables participation from the visitor
    Esimerkkejä, mitä esim tietyt jutut osaa parsia, myös esim streamiaikauluihin voi laittaa jotai
    Tietyt tagit ni esim streami osaa näyttää et nöönöö menossa.
    """
    categories = models.CharField(max_length=255, blank=True)
    """
    esim: Compo,Show
    Major, and possibly, minor category separated by a comma. Categories are used to filter events by different criterias. Possible categories:
    Event: general events. Possible subcategories: Concert, Show
    Compo: demoscene related competitions. Possible subcategories: Deadline, Show, Jury, Prizes
    Game: esports related competitions. Possible subcategories: Semifinals, Finals
    Seminar: seminars. No subcategories for seminars.
    """
    order = models.FloatField(default=0.0)
    location = models.ForeignKey(Location)
    cancel_reason = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    # Muita kuten, palotarkastus jne mitä abyssin

    def default_original_time(self):
        return self.time

    def default_end(self):
        """
        Default end time is start time + 5 minutes so events without a
        duration will show for 5 minutes after.
        """
        return self.time + timedelta(minutes=5)

    def is_active(self):
        """
        Is the event ongoing. An event without end time is considered active 5
        minutes after it started.
        """
        now = datetime.now()

        if not self.end_time:
            return now >= self.time and self.time < now+timedelta(minutes=5)

        return self.time <= now and self.end_time > now

    def is_close_to_end(self):
        """
        In case we want to hilight ending opportunities like voting deadlines.
        """
        return self.is_active() and self.end_time and self.end_time < datetime.now() + timedelta(minutes=15)

    def has_passed(self):
        now = datetime.now()

        if not self.end_time:
            return now > self.time+timedelta(minutes=5)

        return now > self.end_time + timedelta(minutes=15)

    class Meta:
        ordering = ["time", "name"]

import datetime
from django.utils import timezone
from django.db import models


class VendorManger(models.Manager):
    """Class to assist in manipulations of the Vendor model."""

    def update_or_create_vendor(self, name, website):
        """Automate the creation of a vendor with a key_name for fuzzy lookup."""
        key_name = self.make_key_name(name)
        return self.update_or_create(key_name=key_name, name=name, website=website)

    def make_key_name(self, name):
        """Removes whitespace, punctuation, capitalization and returns a string."""
        return ''.join(ch.lower() for ch in name if ch.isalnum())

    def event_counts_since(self, days_ago=30):
        """
        Queries the database to count number of events in days_ago for each vendor.
        Returns a 'django.db.models.query.ValuesQuerySet' of {"vendor":Vendor, "event_count":count}
        """

        def get_date_in_past(days):
            """Return a date that is days in the past from the current date."""
            return timezone.now() - datetime.timedelta(days=days)

        #Filter out events outside the day range
        dates_filtered = VendorEvent.objects.filter(date__gt=get_date_in_past(days=days_ago))

        #
        return dates_filtered.values("vendor").annotate(event_count=Count("id")).order_by("-event_count")

class Vendor(models.Model):
    key_name = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    website = models.URLField()

    objects = VendorManger()

    def __unicode__(self):
        return self.name



class Location(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    def __unicode__(self):
        return self.name


class VendorEvent(models.Model):
    date = models.DateTimeField('event date')
    vendor = models.ForeignKey(Vendor)
    location = models.ForeignKey(Location)

    def __unicode__(self):
        return "%s, %s, %s" % (str(self.date), str(self.vendor), str(self.location))
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

    def get_sorted_event_counts(self, days_ago=30):
        """
        Queries the database to count number of events in days_ago for each vendor.
        Returns a list of {"vendor":Vendor, "event_count":int} sorted in descending order
        by event_count.
        """

        #Note this function could be a bottle neck for the database. However, a cache
        #could easily fix that if need be.

        vendor_and_count = self.get_event_counts(days_ago=days_ago)
        vendor_and_count.sort(reverse=True, key=lambda x: x["event_count"])

        return vendor_and_count

    def get_event_counts(self, days_ago=30):
        vendors = Vendor.objects.all()
        vendor_and_count = []
        
        for vendor in vendors:
            event_count = vendor.events_since(days_ago=days_ago)
            vendor_and_count.append({"vendor":vendor, "event_count":event_count})

        return vendor_and_count

class Vendor(models.Model):
    key_name = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    website = models.URLField()

    objects = VendorManger()

    def events_since(self, days_ago=30):
        def get_date_in_past(days):
            """Return a date that is days in the past from the current date."""
            return timezone.now() - datetime.timedelta(days=days)

        filtered = VendorEvent.objects.filter(vendor=self,date__gt=get_date_in_past(days=days_ago))
        return filtered.count()

    def __unicode__(self):
        return "%s, %s" % (self.name, self.website)


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
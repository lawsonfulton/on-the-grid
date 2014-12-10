from django.utils import timezone
from datetime import datetime, timedelta, time
from django.db import models


class VendorManger(models.Manager):
    """Class to assist in manipulations of the Vendor model."""

    def make_key_name(self, name):
        """
        Removes whitespace, punctuation, capitalization. As well removes
        all occurences of the word 'truck'and returns a string.
        This is to resolve ambiguity in vendor names specified in facebook
        event descriptions.
        """

        #A more complete solution would be to back lookups with a fuzzy
        #search using something like levenshtein distance.
        #However, I have ommited this for the sake of time.
        all_alpha_num = ''.join(ch.lower() for ch in name if ch.isalnum())
        no_truck = all_alpha_num.replace("truck", "").rstrip()

        return no_truck

    def get_by_name(self, name):
        """
        Use a primitive fuzzy search for vendor names.
        If found, return the Vendor object. Otherwise raises a
        django.core.exceptions.DoesNotExist exception.
        """
        key_name = self.make_key_name(name)
        return self.get(pk=key_name)

    def update_or_create_vendor(self, name, website):
        """Automate the creation of a vendor with a key_name for fuzzy lookup."""
        key_name = self.make_key_name(name)
        return self.update_or_create(key_name=key_name, name=name, website=website)

    def get_sorted_event_counts(self, days_ago=30, start_date=timezone.now()):
        """
        Queries the database to count number of events in days_ago for each vendor.
        Returns a list of {"vendor":Vendor, "event_count":int} sorted in descending order
        by event_count.
        """

        #Note this function could be a bottle neck for the database. However, a cache
        #could easily fix that if need be.

        vendor_and_count = self.get_event_counts(days_ago=days_ago, start_date=start_date)
        vendor_and_count.sort(reverse=True, key=lambda x: x["event_count"])

        return vendor_and_count

    def get_event_counts(self, days_ago=30, start_date=timezone.now()):
        """
        Queries the database to count number of events in days_ago for each vendor.
        Returns a list of {"vendor":Vendor, "event_count":int} unsorted.
        """
        vendors = self.all()
        vendor_and_count = []

        for vendor in vendors:
            event_count = vendor.events_since(days_ago=days_ago, start_date=start_date)
            vendor_and_count.append({"vendor":vendor, "event_count":event_count})

        return vendor_and_count

class VendorEventManager(models.Manager):
    """Class to assist in manipulations of the VendorEvent model."""

    def get_by_date_location(self, date, location):
        """
        Return a list of vendors with events that occur on the same day as date
        and at the same location as at location.
        """
        
        return self.filter(location=location,
                           date__startswith=date.date())

    def get_oldest_date(self):
        """Return the event with the lowest date."""
        return self.aggregate(models.Min("date"))["date__min"]

    def get_num_days_of_data(self, days_ago, start_date=timezone.now()):
        """
        Return days_ago or the day-delta for the oldest date in the db if we
        don't have enough data.
        """
        target_date = (start_date - timedelta(days=days_ago)).date()
        oldest_date = self.get_oldest_date().date()
        min_date = max(oldest_date, target_date)

        return (start_date.date() - min_date).days + 1 #plus one for inclusive

class Vendor(models.Model):
    key_name = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    website = models.URLField()

    objects = VendorManger()

    def events_since(self, days_ago=30, start_date=timezone.now()):
        """Return the number of events this vendor has attended since days_ago."""

        end = (start_date + timedelta(days=1)).date() #date__range checks until 00:00 on the end date, so need to add one to include start
        start = (start_date - timedelta(days=days_ago)).date()
        date_range = [start, end]

        filtered = VendorEvent.objects.filter(vendor=self, date__range=date_range)
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

    objects = VendorEventManager()

    def __unicode__(self):
        return "%s, %s, %s" % (str(self.date), str(self.vendor), str(self.location))
import datetime
from django.utils import timezone
from django.db import models


class Vendor(models.Model):
    key_name = models.CharField(max_length=200, primary_key=True)
    display_name = models.CharField(max_length=200, primary_key=True)

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
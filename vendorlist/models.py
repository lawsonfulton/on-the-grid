from django.db import models


class Vendor(models.Model):
    name = models.CharField(max_length=200, primary_key=True)


class Location(models.Model):
    name = models.CharField(max_length=200, primary_key=True)


class VendorEvent(models.Model):
    date = models.DateTimeField('event date')
    vendor = models.ForeignKey(Vendor)
    location = models.ForeignKey(Location)

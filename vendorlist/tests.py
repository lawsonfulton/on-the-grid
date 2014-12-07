import datetime
from django.test import TestCase
from django.utils import timezone
from django.db.models import Count
from vendorlist.models import VendorEvent, Vendor, Location

class DatabaseTestCase(TestCase):
    def setUp(self):
        self.vendors = []
        self.locations = []

        self.vendors.append(Vendor.objects.create(name="Test Vendor 1"))
        self.vendors.append(Vendor.objects.create(name="Test Vendor 2"))

        self.locations.append(Location.objects.create(name="Test Location 1"))
        self.locations.append(Location.objects.create(name="Test Location 2"))

        for i in xrange(100):
            date = timezone.now() - datetime.timedelta(days=i)
            vendor_event = VendorEvent.objects.create(date=date,
                                                      vendor=self.vendors[i%2],
                                                      location=self.locations[i%2])

    def test_filter(self):
        # Entry.objects.filter(mod_date__gt=F('pub_date') + timedelta(days=3))

        def get_date_in_past(days):
            """Return a date that is days in the past from the current date."""
            return timezone.now() - datetime.timedelta(days=days)

        date_restricted = VendorEvent.objects.filter(date__gt=get_date_in_past(days=30))
        vendor_list = date_restricted.values("vendor").annotate(event_count=Count("id")).order_by("-event_count")

        #vendor_list = Vendor.objects.annotate(event_count=Count("vendorevent__vendor")).order_by("-event_count")

        for vendor in vendor_list:
            print str(vendor) + " " + str(vendor)

        #print len(vendor_restricted)   
        #print Vendor.objects.annotate(event_count=Vendor.objects.filter(vendorevent__date__year=timezone.now().year, vendorevent__vendor="Test Vendor 1"))
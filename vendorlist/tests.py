import datetime
from django.test import TestCase
from django.utils import timezone
from django.db.models import Count
from vendorlist.models import VendorEvent, Vendor, Location

from django.core.management import call_command

class DatabaseTestCase(TestCase):
    def setUp(self):
        call_command("update_vendors")                                            location=self.locations[i%2])

    def test_filter(self):
        
        count_list = Vendor.objects.event_counts_since(days_ago=30)
        print count_list

        # Entry.objects.filter(mod_date__gt=F('pub_date') + timedelta(days=3))

        # def get_date_in_past(days):
        #     """Return a date that is days in the past from the current date."""
        #     return timezone.now() - datetime.timedelta(days=days)

        # date_restricted = VendorEvent.objects.filter(date__gt=get_date_in_past(days=30))
        # vendor_list = date_restricted.values("vendor").annotate(event_count=Count("id")).order_by("-event_count")

        # #vendor_list = Vendor.objects.annotate(event_count=Count("vendorevent__vendor")).order_by("-event_count")

        # for vendor in vendor_list:
        #     print str(vendor) + " " + str(vendor)

        #print len(vendor_restricted)   
        #print Vendor.objects.annotate(event_count=Vendor.objects.filter(vendorevent__date__year=timezone.now().year, vendorevent__vendor="Test Vendor 1"))

# class UpdateVendorsTestCase(TestCase):
#     def test_command(self):
#         call_command("update_vendors")
#         for vendor in Vendor.objects.all():
#             print vendor




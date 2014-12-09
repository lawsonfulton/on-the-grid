import datetime, time
from django.test import TestCase
from django.utils import timezone
import dateutil.parser as dateparser
from vendorlist.models import VendorEvent, Vendor, Location
from django.core.management import call_command

class DatabaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        print "Scraping vendor site. "
        call_command("update_vendors", "test")
        call_command("update_vendor_events", "test")

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print "%s: %.3f" % (self.id(), t)


    # def total_events(self, event_counts):
    #     return sum(x["event_count"] for x in event_counts)

    # def test_fullrange(self):
    #     count_list = Vendor.objects.get_sorted_event_counts(days_ago=self.num_days)
    #     self.assertEqual(self.total_events(count_list), self.num_days * self.events_per_day)

    # def test_one_day(self):
    #     count_list = Vendor.objects.get_sorted_event_counts(days_ago=1)
    #     self.assertEqual(self.total_events(count_list), self.events_per_day)

    # def test_month(self):
    #     count_list = Vendor.objects.get_sorted_event_counts(days_ago=30)
    #     self.assertEqual(self.total_events(count_list), self.events_per_day*min(30,self.num_days))

    # def test_scrape_fb(self):
    #     call_command("update_vendor_events", "test")
    #     count_list = Vendor.objects.get_sorted_event_counts(days_ago=30)
    #     self.assertTrue(len(count_list) > 1)

    def test_get_by_date_location(self):
        today = dateparser.parse("2014-12-10")
        location = Location.objects.get(pk="410 Minna St, San Francisco CA")
        events = VendorEvent.objects.get_by_date_location(date=today, location=location)

        vendor_key_names = [event["vendor"] for event in events.values("vendor")]
        actual_key_names = ['peruchi', 'dum', 'theboneyard', 'sajj', 'baconbacon', 'ebbettsgoodtogo']
        
        self.assertEqual(sorted(vendor_key_names), sorted(actual_key_names))

    def test_post_hipchat(self):
        #Need to check by visual inspection
        #Could use api if needed
        call_command("post_to_hipchat", "2014-12-10")




import datetime, time
from django.test import TestCase
from django.utils import timezone
from vendorlist.models import VendorEvent, Vendor, Location

from django.core.management import call_command

class DatabaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        print "Scraping vendor site. "
        call_command("update_vendors")

        vendors = Vendor.objects.all()

        cls.num_days = 1
        cls.events_per_day = 15

        cls.locations = []
        cls.locations.append(Location.objects.create(name="Test Location 1"))
        cls.locations.append(Location.objects.create(name="Test Location 2"))

        print "Generating events"
        for i in xrange(cls.num_days):
            for j in xrange(cls.events_per_day):
                date = timezone.now() - datetime.timedelta(days=i)
                vendor = vendors[(i + j) % len(vendors)]

                vendor_event = VendorEvent.objects.create(date=date,
                                                          vendor=vendor,
                                                          location=cls.locations[i%2])
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print "%s: %.3f" % (self.id(), t)

    def total_events(self, event_counts):
        return sum(x["event_count"] for x in event_counts)

    def test_fullrange(self):
        count_list = Vendor.objects.get_sorted_event_counts(days_ago=self.num_days)
        self.assertEqual(self.total_events(count_list), self.num_days * self.events_per_day)

    def test_one_day(self):
        count_list = Vendor.objects.get_sorted_event_counts(days_ago=1)
        self.assertEqual(self.total_events(count_list), self.events_per_day)

    def test_month(self):
        count_list = Vendor.objects.get_sorted_event_counts(days_ago=30)
        self.assertEqual(self.total_events(count_list), self.events_per_day*min(30,self.num_days))

    def test_scrape_fb(self):
        call_command("update_vendor_events")
        count_list = Vendor.objects.get_sorted_event_counts(days_ago=30)
        self.assertTrue(len(count_list) > 1)

    def test_hipchat_post(self):
        #just make sure it doesn't error
        #could use api to check it was posted.
        call_command("update_vendor_events")
        call_command("post_to_hipchat")


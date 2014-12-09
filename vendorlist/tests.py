import datetime, time
from django.test import TestCase
from django.utils import timezone
import dateutil.parser as dateparser
from vendorlist.models import VendorEvent, Vendor, Location
from django.core.management import call_command
from datetime import timedelta  


class DatabaseTestCase(TestCase):
    today = dateparser.parse("2014-12-10").date() #This is a wednesday

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

    def test_update_vendor_events_worked(self):
        actual_num_events = 647 #No way to get this apriori unless count manually
        added_events = VendorEvent.objects.count()

        self.assertEqual(added_events, actual_num_events)

    def test_update_vendors_worked(self):
        from vendorlist.management.commands.update_vendors import Command
        from collections import Counter

        elements = Command().get_vendor_data_elements(testing_mode=True)
        name_gen = (Command().get_name_website_pair(element)[0] for element in elements)
        expected_count = len(Counter(name_gen))

        added_vendors = Vendor.objects.count()

        self.assertEqual(added_vendors, expected_count)

    def test_date_range(self):
        actual_num_events = 123 #counted explicitly from fb page
        vendor_count_pairs = Vendor.objects.get_sorted_event_counts(days_ago=0, start_date=self.today)

        num_added_events = 0
        for pair in vendor_count_pairs:
            num_added_events += pair["event_count"]

        self.assertEqual(num_added_events, actual_num_events)

    def test_get_by_date_location(self):
        location = Location.objects.get(pk="410 Minna St, San Francisco CA")
        events = VendorEvent.objects.get_by_date_location(date=self.today, location=location)

        vendor_key_names = [event["vendor"] for event in events.values("vendor")]
        actual_key_names = ['peruchi', 'dum', 'theboneyard', 'sajj', 'baconbacon', 'ebbettsgoodtogo']
        
        self.assertEqual(sorted(vendor_key_names), sorted(actual_key_names))

    def test_get_by_date_location_empty(self):
        location = Location.objects.get(pk="410 Minna St, San Francisco CA")
        thursday = self.today + timedelta(1)
        events = VendorEvent.objects.get_by_date_location(date=thursday, location=location)
        vendor_key_names = [event["vendor"] for event in events.values("vendor")]
        actual_key_names = []
        
        self.assertEqual(sorted(vendor_key_names), sorted(actual_key_names))

    def test_post_hipchat(self):
        #Need to check by visual inspection
        #Could use api if needed
        call_command("post_to_hipchat", "2014-12-10")

    def test_get_oldest_date(self):
        expected_oldest_date = datetime.date(2014, 11, 25)
        actual = VendorEvent.objects.get_oldest_date()

        self.assertEqual(actual, expected_oldest_date)

    def test_num_days_of_data(self):
        expected_days = 15
        actual_days = VendorEvent.objects.get_num_days_of_data(30, self.today)

        self.assertEqual(actual_days, expected_days)


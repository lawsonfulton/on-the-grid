from django.core.management.base import BaseCommand, CommandError
from vendorlist.models import Vendor, VendorEvent, Location
from django.conf import settings
from itertools import ifilter

import dateutil.parser as dateparser
import facebook
import urllib2


class Command(BaseCommand):
    """Scrape the facebook event data for OffTheGridSF and add/update it to the database."""

    event_page_url = "https://graph.facebook.com/OffTheGridSF/events"
    help = "Crawls the OffTheGrid facebook event page at %s" % event_page_url

    def handle(self, *args, **options):
        print "Scraping the facebook page..."
        graph = self.connect_to_facebook()
        event_data = self.get_event_data(graph)

        print "Updating the database..."
        #If this is too slow, we could add only new events.
        #However, this will ensure that any event changes will be captured.
        total_events = 0
        for event in event_data:
            total_events += self.add_events_to_db(event)

        print "Success! Added or updated %d events." % total_events

    def connect_to_facebook(self):
        """Use the app keys in the settings to connect to the facebook graph api."""
        try:
            access_token = facebook.get_app_access_token(settings.FACEBOOK_APP_ID,
                                                         settings.FACEBOOK_APP_SECRET)
            graph = facebook.GraphAPI(access_token)
        except urllib2.HTTPError as e:
            raise CommandError("Bad Facebook app id or secret key.")

        return graph

    def get_event_data(self, graph):
        """Query the OffTheGridSF event page and return all event data."""
        try:
            #I'm not sure if there is a limit to the 'limit', but it appears that there are at most
            #115 events stored on the page at the moment.
            response = graph.get_object("OffTheGridSF/events",
                                      limit=10000,
                                      fields=["description", "location", "start_time", "name"])    
        except facebook.GraphAPIError:
            raise CommandError("Couldn't connect to the OffTheGridSF page.")

        return response.get("data", None)

    def add_events_to_db(self, event):
        """
        Takes an event with "description", "location", and "start_time" fields and
        adds a new vendor event for each vendor in the description.
        Any new locations are also added to the Locations table.
        Returns the number of VendorEvents created.
        """
        description = event["description"]
        location_name = event["location"]
        date = dateparser.parse(event["start_time"]).date()

        location, created = Location.objects.update_or_create(name=location_name)
        vendors = self.get_vendors_from_description(description)

        # if "Uptown district boasts" in description:
        #     print {"d":description}
        #     print date
        #     print location_name
        #     print [vendor for vendor in vendors]
        #     raise Exception

        event_count = 0
        for vendor in vendors:
            event, created = VendorEvent.objects.update_or_create(date=date, vendor=vendor, location=location)
            event_count += 1

        return event_count

    def get_vendors_from_description(self, description):
        """
        Parses an event description and returns a generator of Vendor objects.
        Seraching for vendor objects uses a primitive fuzzy search.
        """
        lines =  description.rstrip().split('\n')
        vendors = []

        potential_vendors = (self.get_vendor_from_string(line) for line in lines)
        #Filter out lines that didn't have a vendor
        vendors = ifilter(None, potential_vendors) 

        return vendors

    def get_vendor_from_string(self, string):
        """
        Try multiple manipulations to extract a valid vendor name.
        If one is found, return the corresponding vendor object.
        Otherwise return None.
        """
        try:
            # print Vendor.objects.make_key_name(string)
            return Vendor.objects.get_by_name(string)
        except Vendor.DoesNotExist:
            return None


#TODO
#xParse facebook data and store it
#xpost appropriate data on hip chat
#Update dns
#xSet up cron jobs
#Make sure SECRET_KEY and DEBUG are set to false
#Make a default .env file
#Make it purty
#check heroku region

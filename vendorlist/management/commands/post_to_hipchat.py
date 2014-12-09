from django.core.management.base import BaseCommand, CommandError
from vendorlist.models import Vendor, Location, VendorEvent
from django.utils import timezone
from django.conf import settings

import dateutil.parser as dateparser
import hipchat
import urllib2


class Command(BaseCommand):
    """Post today's food trucks for OFFTHEGRID_LOCATION to the configured HipChat room."""

    help = "Posts a list of vendors to a hipchat room. If an argument is present, attempt to parse date from that."

    def handle(self, *args, **options):
        hipster = hipchat.HipChat(token=settings.HIPCHAT_API_TOKEN)
        room_id = settings.HIPCHAT_ROOM_ID
        bot_name = "OnTheGrid"

        if args:
            today = dateparser.parse(args[0])
        else:
            today = timezone.now()

        todays_vendors = self.get_vendors_by_date(today)
        message = self.make_message_from_vendors(todays_vendors)

        print "Attempting to post message to room id %d" % room_id
        print message

        try:
            hipster.message_room(room_id, bot_name, message, message_format="html")
        except urllib2.HTTPError:
            raise CommandError("Couldn't post message to room id %d." % room_id)
        except urllib2.URLError:
            raise CommandError("Couldn't connect to HipChat. You're probably offline.")

        print "Success!"

    def get_vendors_by_date(self, date=timezone.now()):
        """Return a list of VendorEvent objects with events today at the configured location."""

        location = self.get_offthegrid_location()
        return VendorEvent.objects.get_by_date_location(date=date, location=location)

    def get_offthegrid_location(self):
        """Get a valid location from the settings."""
        loc_name = settings.OFFTHEGRID_LOCATION

        try:
            return Location.objects.get(pk=loc_name)
        except Location.DoesNotExist:
            raise CommandError("Invalid location chosen: %s" % loc_name)

    def make_message_from_vendors(self, vendor_events):
        """Take a list of VendorEvents and return our message for HipChat."""

        message = settings.HIPCHAT_MESSAGE_HEADER + "<br><br>"

        for event in vendor_events:
            message += "- <a href='%s'>%s</a><br>" % (event.vendor.website, event.vendor.name)
        
        if not vendor_events:
            message += "Sorry! No trucks today!<br>"

        message += """<br>Check out how many events these trucks have been to recently \
<a href='%s'>here</a>!""" % settings.VENDOR_LIST_URL

        return message
from django.core.management.base import BaseCommand, CommandError
from vendorlist.models import Vendor
from django.conf import settings
import hipchat
import urllib2

class Command(BaseCommand):
    help = "Posts a list of vendors to a hipchat room."

    def handle(self, *args, **options):
        hipster = hipchat.HipChat(token=settings.HIPCHAT_API_TOKEN)
        room_id = settings.HIPCHAT_ROOM_ID
        bot_name = "OnTheGrid"

        message = str(Vendor.objects.all())

        print "Attempting to post message to room id %d" % room_id
        print message

        try:
            hipster.message_room(room_id, bot_name, message)
        except urllib2.HTTPError:
            raise CommandError("Couldn't post message to room id %d." % room_id)

        print "Success!"
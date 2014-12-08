from django.core.management.base import BaseCommand, CommandError
from vendorlist.models import Vendor
from django.conf import settings

import facebook
import requests

class Command(BaseCommand):
    event_page_url = "https://graph.facebook.com/OffTheGridSF/events"
    help = "Crawls the OffTheGrid facebook event page at %s" % event_page_url

    def handle(self, *args, **options):
        access_token = facebook.get_app_access_token(settings.FACEBOOK_APP_ID,
                                                     settings.FACEBOOK_APP_SECRET)

        graph = facebook.GraphAPI(access_token)

        #I'm not sure if there is a limit to the 'limit', but it appears that there are at most
        #115 events stored on the page at the moment.
        events = graph.get_object("OffTheGridSF/events",
                                  limit=10000,
                                  fields=["description", "location", "start_time", "name"])    
        print events["data"][0]
        #event_id = events["data"][0]["id"]


        print len(events["data"])
        # for event in events["data"]:
        #     print event


#TODO
#Parse facebook data and store it
#post appropriate data on hip chat
#Set up cron jobs
#Make sure SECRET_KEY and DEBUG are set to false
#Make it purty

from django.core.management.base import BaseCommand, CommandError
from vendorlist.models import Vendor

import requests
from lxml import html


class Command(BaseCommand):
    vendor_site = "http://offthegridsf.com/vendors"
    help = "Scrapes %s for new vendors." % vendor_site

    def handle(self, *args, **options):
        """Download the vendor list site and update the Vendor table."""

        request = self.get_website(self.vendor_site)
        vendor_data_elements = self.get_vendor_data_elements(request)

        for vendor_data in vendor_data_elements:
            self.add_vendor_to_db(vendor_data)
        
    def get_website(self, site):
        """Returns a request for site."""
        try:
            request = requests.get(site)
        except requests.exceptions.ConnectionError:
            raise CommandError("Couldn't connect to %s." % site)

        return request

    def get_vendor_data_elements(self, request):
        """Get all the vendor elements from the page and return a list."""
        root = html.fromstring(request.content)
        return root.find_class("otg-vendor-data")

    def add_vendor_to_db(self, vendor_data):
        """Creates a Vendor and adds it to the database."""
        try:
            vendor_name_link = vendor_data.find_class("otg-vendor-name-link")[0]
        except IndexError:
            return

        name = vendor_name_link.text_content()
        website = vendor_name_link.attrib["href"]

        vendor = Vendor.objects.update_or_create_vendor(name=name, website=website)
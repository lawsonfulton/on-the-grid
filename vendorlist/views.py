from django.shortcuts import render
from django.http import HttpResponse

from vendorlist.models import VendorEvent, Vendor, Location


def index(request):
    vendor_event_counts = Vendor.objects.get_sorted_event_counts(days_ago=30)
    context = {'vendor_event_counts': vendor_event_counts, 'days_ago':30}
    return render(request, 'vendorlist/index.html', context)
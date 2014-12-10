from django.shortcuts import render
from django.http import HttpResponse

from vendorlist.models import VendorEvent, Vendor, Location


def index(request):
    days_to_display = 30
    vendor_event_counts = Vendor.objects.get_sorted_event_counts(days_ago=days_to_display)
    print VendorEvent.objects.get_oldest_date()
    days_we_have = VendorEvent.objects.get_num_days_of_data(days_to_display)

    context = {'vendor_event_counts': vendor_event_counts, 'days_ago': days_we_have}
    return render(request, 'vendorlist/index.html', context)





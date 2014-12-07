from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    vendor_list = Vendor.objects.annotate(event_count=)
    VendorEvent.object.filter(vendor_name,)

    return HttpResponse("Hello, world. You're at the polls index.")

def get_vendor_event_counts(day_range=30):
    """
    Queries the database to count number of events in day_range for each vendor.
    Returns a 'django.db.models.query.ValuesQuerySet' of {"vendor":Vendor, "event_count":count}
    """

    def get_date_in_past(days):
        """Return a date that is days in the past from the current date."""
        return timezone.now() - datetime.timedelta(days=days)

    dates_filtered = VendorEvent.objects.filter(date__gt=get_date_in_past(days=day_range))
    return dates_filtered.values("vendor").annotate(event_count=Count("id")).order_by("-event_count")
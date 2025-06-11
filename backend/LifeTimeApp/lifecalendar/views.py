from django.shortcuts import render
from .models import CalendarEntry

# Create your views here.
def calender_list_view(request):
    calender_entries_list = CalendarEntry.objects.order_by("start_date")
    context = {"calender_entries_list":calender_entries_list}
    return render(request,"lifecalendar/entries_list.html", context)


from django.http import JsonResponse
from .models import CalendarEntry
from django.utils.timezone import now
from datetime import timedelta

def calendar_events(request):
    # Optionally filter by current user or week
    entries = CalendarEntry.objects.filter(user=request.user)
    events = []
    for entry in entries:
        events.append({
            "title": entry.name,
            "start": entry.start_date.isoformat(),
            "end": entry.end_date.isoformat(),
            "description": entry.description,
        })
    return JsonResponse(events, safe=False)


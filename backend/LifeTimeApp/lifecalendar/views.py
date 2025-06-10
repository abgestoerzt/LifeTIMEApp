from django.shortcuts import render
from .models import CalendarEntry

# Create your views here.
def calender_list_view(request):
    calender_entries_list = CalendarEntry.objects.order_by("start_date")
    context = {"calender_entries_list":calender_entries_list}
    return render(request,"lifecalendar/entries_list.html", context)
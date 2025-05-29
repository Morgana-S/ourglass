from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Event
# Create your views here.


class LatestEventList(generic.ListView):
    """
    Returns a list of all event objects, ordered by the latest created.
    """
    queryset = Event.objects.all().order_by('-created_on')[:5]
    template_name = 'events/index.html'

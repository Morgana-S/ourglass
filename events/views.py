from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Event
# Create your views here.


class EventList(generic.ListView):
    queryset = Event.objects.all()
    template_name = 'events/event_list.html'

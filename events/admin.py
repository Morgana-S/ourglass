from django.contrib import admin
from .models import Event, Booking
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Event)
class EventAdmin(SummernoteModelAdmin):

    list_display = ('id', 'event_name', 'event_date',)
    search_fields = ['event_name']
    summernote_fields = ('long_description',)


@admin.register(Booking)
class BookingAdmin(SummernoteModelAdmin):

    list_display = ('id', 'event', 'tickets', 'ticketholder',)
    search_fields = ['event', 'ticketholder']


# Register your models here.

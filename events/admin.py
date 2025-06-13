from django.contrib import admin
from .models import Event, Booking, Review
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

@admin.register(Event)
class EventAdmin(SummernoteModelAdmin):

    list_display = ('id', 'event_name', 'event_date', 'event_organiser',
                    'created_on', 'updated_on',)
    search_fields = ['event_name']
    summernote_fields = ('long_description',)
    list_filter = ('event_organiser', 'event_date', 'created_on', 'updated_on')


@admin.register(Booking)
class BookingAdmin(SummernoteModelAdmin):

    list_display = ('id', 'event', 'tickets', 'ticketholder',)
    search_fields = ['event__event_name', 'ticketholder__username']
    list_filter = ('ticketholder', 'event',)


@admin.register(Review)
class ReviewAdmin(SummernoteModelAdmin):

    list_display = ('id', 'event', 'author', 'rating',)
    search_fields = ['author', 'event__event_name']
    list_filter = ('rating', 'author')

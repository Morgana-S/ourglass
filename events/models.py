from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
# Create your models here.


class Event (models.Model):
    event_name = models.CharField(max_length=75)
    event_date = models.DateTimeField()
    is_online = models.BooleanField()
    url_or_address = models.CharField(max_length=100)
    maximum_attendees = models.PositiveSmallIntegerField()
    short_description = models.TextField(max_length=200)
    image = CloudinaryField('image')
    long_description = models.TextField(max_length=3000)
    event_organiser = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.event_name} | Date: {self.event_date}'

    @property
    def current_attendees(self):
        return sum(booking.tickets for booking in self.bookings.all())


class Booking(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='bookings')
    ticketholder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ticketholder')

    NO_OF_TICKETS = [
        (1, 'x1'),
        (2, 'x2'),
        (3, 'x3'),
        (4, 'x4')
    ]
    tickets = models.PositiveSmallIntegerField(choices=NO_OF_TICKETS)

    def __str__(self):
        return f'A booking for {self.event} | Ticketholder: {self.ticketholder} | No. of Tickets: {self.tickets}'

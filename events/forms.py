from django import forms
from django.utils import timezone
from django_summernote.widgets import SummernoteWidget
from datetime import timedelta
from .models import Event, Review, Booking


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'event_name',
            'event_date',
            'image',
            'is_online',
            'url_or_address',
            'maximum_attendees',
            'short_description',
            'long_description',
        ]
        widgets = {
            'event_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Event Name'
                }
            ),
            'event_date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control flatpickr',
                    'placeholder': 'Select date and time'
                }
            ),
            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                    'accept': 'image/*'
                }
            ),
            'is_online': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            ),
            'url_or_address': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'maximum_attendees': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 1,
                    'max': 200,
                    'step': 1,
                    'placeholder': 'Enter a number between 1 - 200'
                }
            ),
            'short_description': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'long_description': SummernoteWidget(),
        }

    def clean_event_date(self):
        event_date = self.cleaned_data.get('event_date')
        now = timezone.now()
        two_years_from_now = now + timedelta(days=730)
        two_years_error = (
            'Event date can not be more than two years from today.'
        )
        if event_date <= timezone.now():
            raise forms.ValidationError("Event date must be in the future.")
        elif event_date > two_years_from_now:
            raise forms.ValidationError(two_years_error)
        return event_date

    def clean_maximum_attendees(self):
        maximum_attendees = self.cleaned_data.get('maximum_attendees')
        attendee_error = (
            'Events with more than 200 attendees are not allowed to be '
            'created manually. Please create your event with 200 attendees '
            'and contact the administrators using the contact us page.'
        )
        if maximum_attendees > 200:
            raise forms.ValidationError(attendee_error)
        elif maximum_attendees < 1:
            raise forms.ValidationError("Event must have at least 1 attendee.")
        return maximum_attendees


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'rating',
            'content',
        ]

    def clean_content(self):
        content = self.cleaned_data.get('content')
        too_short_error = (
            'Your review is too short. Please write a little more!'
        )
        if len(content) < 50:
            raise forms.ValidationError(too_short_error)
        return content


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['tickets']

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        tickets = cleaned_data.get('tickets')
        event_date = self.event.event_date
        now = timezone.now()

        # Skips if there is no info for tickets, user or event
        # used for modifying existing data
        if not tickets or not self.event or not self.user:
            return cleaned_data

        # Checks if the instance already exists, changing projected attendees
        # on this basis
        if self.instance.pk:
            projected_attendees = (
                self.event.current_attendees
                - self.instance.tickets
                + tickets
            )
        else:
            projected_attendees = (
                self.event.current_attendees + tickets
            )

        organiser_error = (
            'You cannot book tickets for your own events.'
        )
        already_booked_error = (
            'You already have tickets to this event.'
        )
        not_enough_spaces_error = (
            "There are not enough spaces left on the event to book this many "
            "tickets."
        )
        past_event_error = (
            'You can not make or change bookings for events that are in the '
            'past.'
        )
        # Checks if the organiser is trying to book their own event
        if self.event.event_organiser == self.user:
            raise forms.ValidationError(organiser_error)

        # Checks if the user is already booked
        if not self.instance.pk and Booking.objects.filter(
            event=self.event,
            ticketholder=self.user
        ).exists():
            raise forms.ValidationError(already_booked_error)

        # Checks available event capacity
        if projected_attendees > self.event.maximum_attendees:
            raise forms.ValidationError(not_enough_spaces_error)

        # Checks Event is not in the past
        if event_date < now:
            raise forms.ValidationError(past_event_error)

        return cleaned_data

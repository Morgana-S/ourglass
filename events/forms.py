from django import forms
from django.utils import timezone
from django_summernote.widgets import SummernoteWidget
from datetime import timedelta
from .models import Event



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
            'event_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            ),
            'long_description': SummernoteWidget()
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

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import EventForm, ReviewForm, BookingForm
from .models import Event, Booking
# Create your tests here.


class TestEventForm(TestCase):
    """
    TestCase for all Event Form tests.
    """

    def setUp(self):
        """
        Creates a reusable setup for testing form data.
        """
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'test',
            content_type='image/jpeg'
        )
        self.form_data = {
            'event_name': 'test event',
            'event_date': (timezone.now() + timedelta(days=2)).strftime(
                '%Y-%m-%d %H:%M:%S'
            ),
            'is_online': False,
            'url_or_address': '123 Tes Street',
            'maximum_attendees': 100,
            'short_description': 'Test Event',
            'long_description': 'Test Event Long Description'
        }

    def test_form_is_valid(self):
        """
        Tests if the form data is valid.
        """
        self.valid_form = EventForm(
            data=self.form_data,
            files={'image': self.image}
        )
        self.assertTrue(self.valid_form.is_valid(), msg='Form is invalid')

    def test_event_date_in_past(self):
        """
        Tests if an event date is in the past. Also confirms that there 
        are errors in the form if the data is incorrect.
        """
        data = self.form_data.copy()
        data['event_date'] = (timezone.now() - timedelta(days=2)).strftime(
            '%Y-%m-%d %H:%M:%S'
        )
        form = EventForm(data=data, files={'image': self.image})
        self.assertFalse(form.is_valid(), msg='event date is valid')
        self.assertIn('event_date', form.errors)

    def test_event_date_too_far_in_future(self):
        """
        Tests if an event date is too far in the future.
        Also confirms that there are errors in the form if the data is
        incorrect.
        """
        data = self.form_data.copy()
        data['event_date'] = (timezone.now() + timedelta(days=1000)).strftime(
            '%Y-%m-%d %H:%M:%S'
        )
        form = EventForm(data=data, files={'image': self.image})
        self.assertFalse(form.is_valid(), msg='event date is valid')
        self.assertIn('event_date', form.errors)

    def test_maximum_attendees_above_limit(self):
        """
        Tests if the event attendees exceed the limit of 200.
        Also confirms that there are errors in the form if the data is
        incorrect.
        """
        data = self.form_data.copy()
        data['maximum_attendees'] = 300
        form = EventForm(data=data, files={'image': self.image})
        self.assertFalse(form.is_valid(), msg='number of attendees is valid')
        self.assertIn('maximum_attendees', form.errors)

    def test_maximum_attendees_below_limit(self):
        """
        Tests if the event attendees is below the limit of 1.
        Also confirms that there are errors in the form if the data is
        incorrect.
        """
        data = self.form_data.copy()
        data['maximum_attendees'] = 0
        form = EventForm(data=data, files={'image': self.image})
        self.assertFalse(form.is_valid(), msg='number of attendees is valid')
        self.assertIn('maximum_attendees', form.errors)

    def test_missing_required_fields(self):
        """
        Tests if the form is valid when required fields are missing.
        Also confirms that there are errors in the form if the data is
        incorrect.
        """
        form = EventForm(data={}, files={})
        self.assertFalse(
            form.is_valid(),
            msg='form is valid without req fields'
        )
        required_fields = [
            'event_name', 'event_date', 'image', 'url_or_address',
            'maximum_attendees', 'short_description', 'long_description'
        ]
        for field in required_fields:
            self.assertIn(field, form.errors)

    def test_is_online_checkbox_true(self):
        """
        Tests if the checkbox for is_online is marked as true.
        """
        data = self.form_data.copy()
        data['is_online'] = True
        form = EventForm(data=data, files={'image': self.image})
        self.assertTrue(form.is_valid())

    def test_is_online_checkbox_false(self):
        """
        Tests if the checkbox for is_online is marked as false.
        """
        data = self.form_data.copy()
        data['is_online'] = False
        form = EventForm(data=data, files={'image': self.image})
        self.assertTrue(form.is_valid())


class TestReviewForm(TestCase):
    """
    TestCase for all Review Form Tests.
    """

    def setUp(self):
        testContent = (
            "This event was amazing! It's also really, really easy to test!"
        )
        self.valid_data = {
            'rating': 4,
            'content': testContent
        }
        self.short_content_data = {
            'rating': 4,
            'content': 'Test'
        }
        self.missing_data = {
            'rating': '',
            'content': ''
        }

    def test_valid_review_form(self):
        """
        Tests if the form data is valid.
        """
        form = ReviewForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), msg='Form is not valid')

    def test_review_content_too_short(self):
        """
        Tests if the review content is too short.
        """
        form = ReviewForm(data=self.short_content_data)
        self.assertFalse(form.is_valid(), msg='Content length is acceptable')

    def test_review_missing_fields(self):
        """
        Tests if the form is missing fields. Also confirms if there are 
        errors in the form fields when submitted.
        """
        form = ReviewForm(data=self.missing_data)
        self.assertFalse(form.is_valid(), msg='Form data is valid')
        self.assertIn('rating', form.errors)
        self.assertIn('content', form.errors)


class TestBookingForm(TestCase):
    """
    TestCase for all Booking Form Tests.
    """
    def setUp(self):
        self.organiser = User.objects.create_user(
            username='organiser',
            password='pass'
            )
        self.attendee = User.objects.create_user(
            username='attendee',
            password='pass'
        )
        self.another_attendee = User.objects.create_user(
            username='another_attendee',
            password='pass'
        )
        self.valid_event = Event.objects.create(
            event_name='Test Event',
            event_date=timezone.now() + timedelta(days=5),
            event_organiser=self.organiser,
            maximum_attendees=10,
            is_online=True,
            url_or_address='Online',
            short_description='Test Description',
            long_description='Test Description Long Version'
        )

    def test_valid_booking_form(self):
        """
        Tests if the booking form is valid.
        """
        form = BookingForm(
            data={
                'tickets': 2
            },
            event=self.valid_event,
            user=self.attendee
        )
        self.assertTrue(form.is_valid(), msg='form is not valid')

    def test_booking_own_event_invalid(self):
        """
        Tests whether a user can book their own event. Also confirms
        whether the user receives the error about booking their own events.
        """
        form = BookingForm(
            data={'tickets':1},
            event=self.valid_event,
            user=self.organiser
        )
        self.assertFalse(form.is_valid(), msg='form is valid')
        self.assertIn(
            'You cannot book tickets for your own events.',
            form.errors['__all__']
            )

    def test_double_booking_invalid(self):
        """
        Tests that users cannot book an event again if an existing booking
        is already in place. Also confirms whether the user is provided the
        'already has tickets' error in the form.
        """
        Booking.objects.create(
            event=self.valid_event, ticketholder=self.attendee, tickets=2
        )
        form = BookingForm(
            data={'tickets':1},
            event=self.valid_event,
            user=self.attendee
        )
        self.assertFalse(form.is_valid(), msg='form is valid')
        self.assertIn(
            'You already have tickets to this event.',
            form.errors['__all__']
        )

    def test_booking_exceeds_capacity(self):
        """
        Tests whether a user can make a booking if there are not enough tickets
        left to book. Also confirms whether the user receives the
        not_enough_spaces_error when trying to book like this.
        """
        not_enough_spaces_error = (
            "There are not enough spaces left on the event to book this many "
            "tickets."
        )
        Booking.objects.create(
            event=self.valid_event,
            ticketholder=self.another_attendee,
            tickets=9
        )
        form = BookingForm(
            data={'tickets': 3},
            event=self.valid_event,
            user=self.attendee
        )
        self.assertFalse(form.is_valid(), msg='form is valid')
        self.assertIn(
            not_enough_spaces_error,
            form.errors['__all__']
            )

    def test_booking_past_event_invalid(self):
        """
        Tests whether the user is able to book a past event. Also tests
        whether the user receives the error about booking past events.
        """
        past_event_error = (
            'You can not make or change bookings for events that are in the '
            'past.'
        )
        self.valid_event.event_date = timezone.now() - timedelta(days=1)
        self.valid_event.save()
        form = BookingForm(
            data={'tickets': 1},
            event=self.valid_event,
            user=self.attendee
        )
        self.assertFalse(form.is_valid(), msg='form is valid')
        self.assertIn(past_event_error, form.errors['__all__'])

from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import EventForm, ReviewForm
# Create your tests here.


class TestEventForm(TestCase):
    """
    Test Case for all Event Form tests.
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

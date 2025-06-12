from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Event, Booking, Review
# Create your tests here.


class LatestEventListTests(TestCase):
    """
    TestCase for the LatestEventList View.
    """

    def setUp(self):
        """
        Creates a user, and 7 different events for that user.
        """
        self.organiser = User.objects.create_user(
            username='organiser',
            email='organiser@testemail.com',
            password='pass'
        )
        for i in range(7):
            Event.objects.create(
                event_name=f"Event {i}",
                event_date=timezone.now() + timezone.timedelta(days=i+1),
                created_on=timezone.now() - timezone.timedelta(days=i),
                image='test.jpg',
                event_organiser=self.organiser,
                is_online=True,
                maximum_attendees=10,
                short_description=f"Short desc {i}",
                long_description=f"Long desc {i}",
            )

    def test_view_status_code_and_template(self):
        """
        Tests whether the request is successful and whether the right template
        is used.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200,)
        self.assertTemplateUsed(response, 'events/index.html')

    def test_view_context_contains_latest_5_events(self):
        """
        Tests whether the event list contains five events.
        """
        response = self.client.get(reverse('index'))
        events = response.context['event_list']
        self.assertEqual(len(events), 5)

    def test_events_ordered_by_created_on(self):
        """
        Tests the events in the event_list are ordered by created_on date.
        """
        response = self.client.get(reverse('index'))
        events = list(response.context['event_list'])
        for i in range(len(events) - 1):
            self.assertTrue(events[i].created_on >= events[i + 1].created_on)


class MyEventsDashBoardViewTests(TestCase):
    """
    TestCase for MyEventsDashboardView.
    """

    def setUp(self):
        """
        Creates a user, logs them in, and then creates future and past events
        with bookings and a review for a past booking.
        """
        self.user = User.objects.create_user(
            username='testuser'
            password='pass'
        )
        self.another_user = User.objects.create_user(
            username='anothertestuser'
            password='pass'
        )
        self.client.login(username='testuser', password='pass')
        self.future_event = Event.objects.create(
            event_name="Future Event",
            event_date=timezone.now() + timezone.timedelta(days=5),
            event_organiser=self.user,
            image='test.jpg',
            url_or_address='123 Test Street',
            is_online=False,
            maximum_attendees=10,
            short_description="Future short description",
            long_description="Future long description",
        )
        self.past_event = Event.objects.create(
            event_name="Past Event",
            event_date=timezone.now() - timezone.timedelta(days=5),
            event_organiser=self.user,
            image='test.jpg',
            url_or_address='123 Test Street',
            is_online=False,
            maximum_attendees=10,
            short_description="Past short description",
            long_description="Past long description",
        )
        self.other_future_event = Event.objects.create(
            event_name="Future Event",
            event_date=timezone.now() + timezone.timedelta(days=5),
            event_organiser=self.another_user,
            image='test.jpg',
            url_or_address='123 Test Street',
            is_online=False,
            maximum_attendees=10,
            short_description="Future short description",
            long_description="Future long description",
        )
        self.other_past_event = Event.objects.create(
            event_name="Past Event",
            event_date=timezone.now() - timezone.timedelta(days=5),
            event_organiser=self.another_user,
            image='test.jpg',
            url_or_address='123 Test Street',
            is_online=False,
            maximum_attendees=10,
            short_description="Past short description",
            long_description="Past long description",
        )
        self.future_booking = Booking.objects.create(
            event=self.other_future_event,
            ticketholder=self.user,
            tickets=1
        )
        self.past_booking = Booking.objects.create(
            event=self.other_past_event,
            ticketholder=self.user,
            tickets=2
        )
        self.review = Review.objects.create(
            event=self.other_past_event,
            author=self.user,
            rating=5,
            content="A really good event, very insightful!",
            approved=True
        )

    def test_dashboard_view_status_and_template(self):
        response = self.client.get(reverse('my-events'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/my-events.html')

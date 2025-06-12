from django.contrib.auth.models import User
from django.contrib.messages import get_messages
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
        organised by both the user and another user, as well as a review
        for a past event.
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='pass'
        )
        self.another_user = User.objects.create_user(
            username='anothertestuser',
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
        """
        Tests whether the request is successful and whether the right template
        is used.
        """
        response = self.client.get(reverse('my-events'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/my-events.html')

    def test_dashboard_context_includes_future_booking(self):
        """
        Tests whether a future booking appears in the context for the view.
        """
        response = self.client.get(reverse('my-events'))
        bookings = response.context['bookings'].object_list
        self.assertIn(self.future_booking, bookings)

    def test_dashboard_context_includes_previous_bookings(self):
        """
        Tests whether a previous booking appears in the context for the view.
        """
        response = self.client.get(reverse('my-events'))
        previous = response.context['previous_bookings'].object_list
        self.assertIn(self.past_booking, previous)

    def test_dashboard_context_includes_organised_events(self):
        """
        Tests whether the context includes events organised by the user.
        """
        response = self.client.get(reverse('my-events'))
        organised = response.context['organised_events'].object_list
        self.assertIn(self.future_event, organised)

    def test_dashboard_previous_bookings_has_review_annotation(self):
        """
        Tests whether a previous booking that has been reviewed is annotated
        to show that it has been reviewed.
        """
        response = self.client.get(reverse('my-events'))
        previous = response.context['previous_bookings'].object_list
        booking_with_review = next(
            (b for b in previous if b.id == self.past_booking.id), None)
        self.assertIsNotNone(booking_with_review)
        self.assertTrue(hasattr(booking_with_review, 'has_review'))
        self.assertTrue(booking_with_review.has_review)

    def test_redirect_if_not_logged_in(self):
        """
        Tests if an anonymous user is redirected to the account page when not
        logged in.
        """
        self.client.logout()
        response = self.client.get(reverse('my-events'))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response, f'/accounts/login/?next={reverse("my-events")}')


class EventDetailViewTests(TestCase):
    """
    TestCase for the event_detail View.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='pass'
        )
        self.another_user = User.objects.create_user(
            username='anotheruser',
            password='pass'
        )
        self.event = Event.objects.create(
            event_name='Test Event',
            event_date=timezone.now() + timezone.timedelta(days=3),
            created_on=timezone.now(),
            image='test.jpg',
            event_organiser=self.user,
            is_online=True,
            maximum_attendees=100,
            short_description='Short description',
            long_description='Long description',
        )
        self.url = reverse('event-detail', args=[self.event.id])

    def test_event_detail_view_status_and_template(self):
        """
        Tests whether the request is successful and whether the right template
        is used.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event-detail.html')

    def test_event_context_for_user_with_booking(self):
        """
        Logs the user in, creates a booking for the event in the user's name,
        and confirms whether the user has a booking according to the context,
        as well as confirming how many tickets they have.
        """
        self.client.login(username='test', password='pass')
        Booking.objects.create(
            event=self.event,
            ticketholder=self.user,
            tickets=2
        )
        response = self.client.get(self.url)
        context = response.context
        self.assertTrue(context['user_has_booking'])
        self.assertEqual(context['user_tickets'], 2)

    def test_event_context_user_has_reviewed(self):
        """
        Logs a user in, creates a review for the event, and then checks to see
        if the context for whether the user has reviewed the event is passed
        correctly.
        """
        self.client.login(username='anotheruser', password='pass')
        Review.objects.create(
            event=self.event,
            author=self.another_user,
            rating=4,
            content='Great event!'
        )
        response = self.client.get(self.url)
        self.assertTrue(response.context['user_has_reviewed'])

    def test_event_context_past_event(self):
        """
        Tests whether the past_event context is registering correctly.
        """
        self.event.event_date = timezone.now() - timezone.timedelta(days=1)
        self.event.save()
        response = self.client.get(self.url)
        self.assertTrue(response.context['past_event'])

    def test_review_pagination(self):
        """
        Creates 15 reviews for the event, then tests whether the pagination
        is working correctly for the reviews.
        """
        for i in range(15):
            Review.objects.create(
                event=self.event,
                author=self.another_user,
                rating=5,
                content=f'Review {i}'
            )
        response = self.client.get(self.url)
        reviews = response.context['reviews']
        self.assertEqual(reviews.paginator.num_pages, 2)
        self.assertEqual(reviews.paginator.count, 15)
        self.assertEqual(len(reviews.object_list), 9)
        response_page_2 = self.client.get(self.url + '?page=2')
        reviews_page_2 = response_page_2.context['reviews']
        self.assertEqual(len(reviews_page_2.object_list), 6)


class TestLogoutView(TestCase):
    """
    TestCase for the logout View.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='pass'
        )
        self.logout_url = reverse('logout')
        self.index_url = reverse('index')
        self.event = Event.objects.create(
            event_name="Test Event",
            event_date=timezone.now() + timezone.timedelta(days=5),
            event_organiser=self.user,
            image='test.jpg',
            url_or_address='123 Test Street',
            is_online=False,
            maximum_attendees=10,
            short_description="Test short description",
            long_description="Test long description",
        )

    def test_logs_user_out_and_redirects(self):
        """
        Logs the user in with the above details, checks whether the user
        is authenticated, then logs the user out and checks again
        whether the user is authenticated. Also checks whether the logout
        view redirects to the index page.
        """
        self.client.login(username='test', password='pass')
        response = self.client.get(self.index_url)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        response = self.client.get(self.logout_url, follow=True)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, self.index_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(
            "You have been logged out." in str(m) for m in messages
        )
        )

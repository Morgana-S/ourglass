from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from unittest.mock import patch
from .models import Event, Booking, Review
from .forms import EventForm, ReviewForm
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


class TestCreateEventView(TestCase):
    """
    TestCase for the create_event View.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='pass'
        )
        self.url = reverse('create-event')

    def test_get_create_event_view_status_and_template(self):
        """
        Logs the user in, then tests the request goes through
        okay and that the correct template is used.
        """
        self.client.login(username='test', password='pass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/create-event.html')
        self.assertIsInstance(response.context['form'], EventForm)

    @patch('cloudinary.uploader.upload')
    def test_post_creates_valid_event(self, mock_upload):
        """
        Logs the user in, creates a mock upload for the CloudinaryField image,
        then confirms that the form redirects to the my-events page,
        checks that the new event exists, and confirms whether
        the user receives a message about the event being created.
        """
        self.client.login(username='test', password='pass')
        mock_upload.return_value = {
            'url': 'http://res.cloudinary.com/fake-image.jpg',
            'public_id': 'fake-id',
            'version': 1,
            'type': 'upload',
            'format': 'jpg',
            'resource_type': 'image',
        }
        image = SimpleUploadedFile(
            name='test.jpg',
            content=b'test',
            content_type='image/jpeg'
        )
        form_data = {
            'event_name': 'Test Event',
            'event_date': (
                timezone.now() + timezone.timedelta(days=5)
            ).strftime(
                '%Y-%m-%d %H:%M:%S'
            ),
            'event_organiser': self.user,
            'image': image,
            'url_or_address': '123 Test Street',
            'is_online': False,
            'maximum_attendees': 10,
            'short_description': 'Test short description',
            'long_description': 'Test long description',
        }
        response = self.client.post(self.url, form_data, follow=True)
        self.assertRedirects(response, reverse('my-events'))
        self.assertTrue(Event.objects.filter(event_name='Test Event').exists())
        messages = list(response.context['messages'])
        self.assertIn('Congratulations', str(messages[0]))

    def test_post_invalid_data_shows_error(self):
        """
        Tests whether the response status is correct if the user posts a form
        with invalid data, and that the error appears in the form. Also
        ensures the user gets a message advising them that the event was not
        created.
        """
        self.client.login(username='test', password='pass')
        invalid_data = {
            'event_name': '',
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context['form']
        self.assertEqual(response.status_code, 200)
        self.assertFormError(form, 'event_name', 'This field is required.')
        messages = list(response.context['messages'])
        self.assertIn('Your event was not created', str(messages[0]))

    def test_unauthenticated_user_redirected(self):
        """
        Tests whether an anonymous user gets redirected to the index page,
        and whether they receive a message indicating they are not currently
        logged in.
        """
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, reverse('index'))
        messages = list(response.context['messages'])
        self.assertIn('not currently logged in', str(messages[0]))


class TestEditEventView(TestCase):
    """
    TestCase for edit_event View.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='pass',
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
        self.url = reverse('edit-event', args=[self.event.id])

    def test_get_edit_event_form(self):
        """
        Logs the user in, then attempts to get the edit-event form for the
        above event. Checks if the get request goes through properly,
        the right template is used, the form is passed to the context
        and that the form for the instance is for this event.
        """
        self.client.login(username='test', password='pass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/edit-event.html')
        self.assertIn('form', response.context)
        self.assertEqual(response.context['form'].instance, self.event)

    def test_post_valid_data_updates_event(self):
        """
        Logs the user in, attempts to post new form data to the database for
        the existing event, and then checks if the event instance has been
        updated with new form data. Also checks that the user has been
        informed that the event is updated.
        """
        self.client.login(username='test', password='pass')
        new_name = 'Updated Event Name'
        response = self.client.post(
            self.url,
            {
                'event_name': new_name,
                'event_date': (
                    timezone.now() + timezone.timedelta(days=5)
                ).strftime(
                    '%Y-%m-%d %H:%M:%S'
                ),
                'image': 'test.jpg',
                'url_or_address': 'New Address',
                'is_online': False,
                'maximum_attendees': 20,
                'short_description': 'Updated short',
                'long_description': 'Updated long',
            },
            follow=True
        )
        self.event.refresh_from_db()
        self.assertEqual(self.event.event_name, new_name)
        self.assertRedirects(response, reverse(
            'event-detail', args=[self.event.id]))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Your event has now been updated.', str(messages[0]))

    def test_post_invalid_data_shows_error(self):
        """
        Logs the user in, tries to post data that would be invalid to the form,
        checks if the response code is a get request, checks the template is
        provided to the view, and that the form has been updated with the
        required fields, and that the user receives a message advising that
        their event was not updated successfully.
        """
        self.client.login(username='test', password='pass')
        response = self.client.post(
            self.url,
            {
                'event_name': '',
            },
            follow=True
        )
        form = response.context['form']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/edit-event.html')
        self.assertFormError(
            form,
            'event_name',
            'This field is required.')
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            'Your event was not updated successfully.',
            str(messages[0])
        )

    def test_unauthenticated_user_redirected(self):
        """
        Does not log the user in, attempts to load the edit-event page.
        Checks if the user is redirected to the index page and that
        they receive a message about not being logged in.
        """
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            'You cannot edit an event as you are not currently logged in.',
            str(messages[0])
        )

    def test_user_cannot_edit_other_users_event(self):
        """
        Creates a new user, logs in as that user and attempts to
        post new data to the view with the event name edited. Then
        obtains data from the database and confirms that the event wasn't
        updated. Also confirms to the user that the event wasn't updated.
        """
        # not accessed directly, but used in the login
        other_user = User.objects.create_user(
            username='other',
            password='pass'
        )
        self.client.login(username='other', password='pass')
        response = self.client.post(
            self.url,
            {
                'event_name': 'new event name'
            },
            follow=True
        )
        self.event.refresh_from_db()
        self.assertNotEqual(self.event.event_name, 'new event name')
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Your event was not updated successfully.',
                      str(messages[0]))


class TestDeleteEventView(TestCase):
    """
    TestCase for the delete_event view.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='pass',
        )
        self.other_user = User.objects.create_user(
            username='other',
            password='pass',
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
        self.url = reverse('delete-event', args=[self.event.id])

    def test_event_deleted_by_organiser(self):
        """
        Logs the user in, posts the delete url for the event, then checks
        the user is redirected to the my-events page, whether the event still
        exists, and that the user received a message about the event being
        deleted.
        """
        self.client.login(username='test', password='pass')
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, reverse('my-events'))
        self.assertFalse(Event.objects.filter(id=self.event.id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('This event has now been deleted.', str(messages[0]))

    def test_event_not_deleted_by_other_user(self):
        """
        Logs a different user in than the event organiser, attempts to delete
        the event. Confirms that the user is redirected to the event-detail
        page and that they receive a message indicating they don't have
        permission to delete the event.
        """
        self.client.login(username='other', password='pass')
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, reverse(
            'event-detail', args=[self.event.id]))
        self.assertTrue(Event.objects.filter(id=self.event.id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            'You do not have permission to delete this event.',
            str(messages[0])
        )

    def test_event_not_deleted_by_unauthenticated_user(self):
        """
        Tests that anonymous users who try to delete events
        are directed back to the index page, with a message about them
        not being logged in.
        """
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(Event.objects.filter(id=self.event.id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            'You cannot delete an event as you are not currently logged in.',
            str(messages[0])
        )


class TestReviewEventView(TestCase):
    """
    TestCase for the review_event View.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='pass'
        )
        self.other_user = User.objects.create_user(
            username='other',
            password='pass'
        )
        self.event = Event.objects.create(
            event_name='Test Event',
            event_date=timezone.now() - timezone.timedelta(days=3),
            created_on=timezone.now(),
            image='test.jpg',
            event_organiser=self.other_user,
            is_online=True,
            maximum_attendees=100,
            short_description='Short description',
            long_description='Long description',
        )
        self.url = reverse('review-event', args=[self.event.id])

    def test_get_review_form_authenticated_user(self):
        """
        Logs the user in, creates a booking for the event and checks if the
        user is then able to access the review-event view.
        """
        self.client.login(username='test', password='pass')
        Booking.objects.create(
            event=self.event,
            ticketholder=self.user,
            tickets=2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/review-event.html')
        self.assertIsInstance(response.context['form'], ReviewForm)

    def test_review_submission_by_eligible_user(self):
        """
        Logs the user in, creates a booking for the event, posts a review
        and checks to see if the user is redirected to the event-detail page,
        Checks the number of reviews increase to 1, and confirms the review
        details match those of the user. Also confirms the user receives a
        message advising them the review has been submitted.
        """
        self.client.login(username='test', password='pass')
        Booking.objects.create(
            event=self.event,
            ticketholder=self.user,
            tickets=2)
        post_data = {
            'rating': 5,
            'content': 'Amazing event! Would love to come to the next one!!'
        }
        response = self.client.post(self.url, post_data, follow=True)
        self.assertRedirects(
            response,
            reverse('event-detail', args=[self.event.id])
        )
        self.assertEqual(Review.objects.count(), 1)
        review = Review.objects.first()
        self.assertEqual(review.event, self.event)
        self.assertEqual(review.author, self.user)
        self.assertFalse(review.approved)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Thank you, your review has now been sent',
                      str(messages[0]))

    def test_review_blocked_if_already_reviewed(self):
        """
        Logs the user in, creates a booking for the event and a review to act
        as an existing review. Then tries to create another review and checks
        to make sure the review doesn't go through, and that the user receives
        a message advising them that the new review was unsuccessful.
        """
        self.client.login(username='test', password='pass')
        Booking.objects.create(
            event=self.event,
            ticketholder=self.user,
            tickets=2)
        Review.objects.create(
            event=self.event,
            author=self.user,
            rating=4,
            content='Old review for the same event, test test test test test',
            approved=True)
        post_data = {
            'rating': 5,
            'content': 'Duplicate attempt at review, test test test test test'
        }
        response = self.client.post(self.url, post_data, follow=True)
        self.assertRedirects(response, reverse(
            'event-detail', args=[self.event.id]))
        self.assertEqual(Review.objects.count(), 1)  # still only the old one
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('you cannot leave a review for this event',
                      str(messages[0]))

    def test_review_blocked_if_user_has_no_booking(self):
        """
        Logs the user in, but does not create a booking for the user. Then
        tries to post a review to the event - checks if the user is redirected,
        whether the review count increases, and that the user receives a
        message advising them the review didn't work.
        """
        self.client.login(username='test', password='pass')
        post_data = {
            'rating': 5,
            'content': 'Trying without booking, test test test test test test'
        }
        response = self.client.post(self.url, post_data, follow=True)
        self.assertRedirects(response, reverse(
            'event-detail', args=[self.event.id]))
        self.assertEqual(Review.objects.count(), 0)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('you cannot leave a review for this event',
                      str(messages[0]))

    def test_review_form_invalid_data(self):
        """
        Logs the user in and creates a booking for them, then attempts
        to post a review without any content or rating. Checks that the user
        is redirected and receives a message advising them the review
        was unsuccessful.
        """
        self.client.login(username='test', password='pass')
        Booking.objects.create(
            event=self.event,
            ticketholder=self.user,
            tickets=2)
        post_data = {'rating': '', 'content': ''}
        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/review-event.html')
        # single quote in the below assert escaped
        self.assertContains(
            response, "Sorry, your review wasn&#x27;t able to be submitted")
        self.assertEqual(Review.objects.count(), 0)


def test_redirects_if_user_not_logged_in(self):
    """
    Keeps the user anonymous, then attempts to navigate to the view for leaving
    a review. Checks to see if the user is redirected to the index page, and
    receives a message advising that they can't leave a review.
    """
    response = self.client.get(self.url, follow=True)
    self.assertRedirects(response, reverse('index'))
    messages = list(get_messages(response.wsgi_request))
    self.assertIn(
        'You cannot review an event as you are not currently logged in',
        str(messages[0])
    )


class TestEditReviewView(TestCase):
    """
    TestCase for edit_review View.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='pass'
        )
        self.other_user = User.objects.create_user(
            username='other',
            password='pass'
        )
        self.event = Event.objects.create(
            event_name='Test Event',
            event_date=timezone.now() - timezone.timedelta(days=3),
            created_on=timezone.now(),
            image='test.jpg',
            event_organiser=self.other_user,
            is_online=True,
            maximum_attendees=100,
            short_description='Short description',
            long_description='Long description',
        )
        self.review = Review.objects.create(
            event=self.event,
            author=self.user,
            rating=4,
            content='This was a great event with lots of fun! Test test test',
            approved=True
        )
        self.url = reverse('edit-review', args=[self.review.id])

    def test_redirects_unauthenticated_user(self):
        """
        Attempts to access the review url as an anonymous user. Checks that
        the user is redirected to the index page and receives the not logged
        in error.
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            'You cannot edit a review as you are not currently logged in',
            str(messages[0])
        )

    def test_authenticated_non_author_redirected(self):
        """
        Logs another user in, then attempts to edit the original user's review.
        Checks that the user is redirected to the event-detail page and is
        shown a message about not being able to update the review.
        """
        self.client.login(username='other', password='pass')
        response = self.client.post(self.url, {
            'rating': 5,
            'content': 'Trying to edit someone else\'s review.'
        })
        self.assertRedirects(response, reverse(
            'event-detail', args=[self.event.id]))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            'Review was unable to be updated.',
            [m.message for m in messages]
        )

    def test_author_get_request_renders_form(self):
        """
        Logs the user in, then tests that they can get the edit-review view,
        that it uses the right template, and that the form context is passed
        to the template. Also checks that the form instance matches the
        existing review.
        """
        self.client.login(username='test', password='pass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/edit-review.html')
        self.assertIsInstance(response.context['form'], ReviewForm)
        self.assertEqual(response.context['form'].instance, self.review)


def test_valid_post_by_author_updates_review(self):
    """
    Logs the user in, then updates the review and posts it. Checks that the
    rating is updated, the review content is updated, and that the review
    is now no longer approved. Also checks the messages to ensure the user
    receives a succcess message.
    """
    self.client.login(username='test', password='pass')
    response = self.client.post(
        self.url,
        {
            'rating': 3,
            'content': 'Long text content review test test test test test test'
        }
    )
    self.assertRedirects(
        response,
        reverse('event-detail', args=[self.event.id])
    )
    self.review.refresh_from_db()
    self.assertEqual(self.review.rating, 3)
    self.assertEqual(
        self.review.content,
        'Long text content review test test test test test test'
    )
    self.assertFalse(self.review.approved)
    messages = list(get_messages(response.wsgi_request))
    self.assertIn(
        'Your updated review is now awaiting approval.',
        [m.message for m in messages]
    )


def test_invalid_post_shows_error(self):
    """
    Logs the user in, then attempts to update the review with invalid rating
    and content. Checks that the user is redirected back to the event-detail
    page, that the review hasn't been updated, and that the user was informed
    in the messages that the review couldn't be updated.
    """
    self.client.login(username='test', password='pass')
    response = self.client.post(
        self.url,
        {
            'rating': '',
            'content': 'Too short'
        }
    )
    self.assertRedirects(response, reverse(
        'event-detail', args=[self.event.id]))
    self.review.refresh_from_db()
    self.assertNotEqual(self.review.content, 'Too short')
    messages = list(get_messages(response.wsgi_request))
    self.assertIn('Review was unable to be updated.',
                  [m.message for m in messages])


class TestDeleteReviewView(TestCase):
    """
    TestCase for the delete_review View.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='pass'
        )
        self.other_user = User.objects.create_user(
            username='other',
            password='pass'
        )
        self.event = Event.objects.create(
            event_name='Test Event',
            event_date=timezone.now() - timezone.timedelta(days=3),
            created_on=timezone.now(),
            image='test.jpg',
            event_organiser=self.other_user,
            is_online=True,
            maximum_attendees=100,
            short_description='Short description',
            long_description='Long description',
        )
        self.review = Review.objects.create(
            event=self.event,
            author=self.user,
            rating=4,
            content='This was a great event with lots of fun! Test test test',
            approved=True
        )
        self.url = reverse('delete-review', args=[self.review.id])

    def test_author_can_delete_review(self):
        """
        Logs the user in, then attempts to delete the review. Checks that the
        user is redirected to the event-detail page, that the review
        no longer exists, and that the user gets a message confirming the
        review has been deleted.
        """
        self.client.login(username='test', password='pass')
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(
            response,
            reverse('event-detail', args=[self.event.id])
        )
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Your review has now been deleted.',
                      [msg.message for msg in messages])

    def test_non_author_cannot_delete_review(self):
        """
        Logs another user in, then attempts to delete the review. Checks that
        the user is redirected back to the event-detail page, that the review
        still exists, and that the user gets an error message.
        """
        self.client.login(username='other', password='pass')
        response = self.client.post(self.url, follow=True)
        self.assertTrue(Review.objects.filter(id=self.review.id).exists())
        self.assertRedirects(
            response,
            reverse('event-detail', args=[self.event.id])
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            "You can not delete other people's reviews.",
            [msg.message for msg in messages]
        )

    def test_anonymous_user_redirected(self):
        """
        Does not log the user in, and then attempts to delete the review.
        Checks that the review still exists and that the user is redirected
        to the index page, with a message saying you can't delete a review
        if not logged in.
        """
        response = self.client.post(self.url, follow=True)
        self.assertTrue(Review.objects.filter(id=self.review.id).exists())
        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            'You can not delete a review if you are not logged in.',
            str(messages[0])
        )

    def test_get_request_does_not_delete(self):
        """
        Tests that a GET response does not delete the review. Should redirect
        user to the index page and advise them of an invalid request through
        message.
        """
        self.client.login(username='test', password='pass')
        # not accessed directly but still called to check the GET request
        response = self.client.get(self.url, follow=True)
        self.assertTrue(Review.objects.filter(id=self.review.id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            'Invalid request type (GET). Please contact the site',
            str(messages[0])
        )


class TestAllEventsView(TestCase):
    """
    TestCase for all_events View.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='pass'
        )
        self.organiser = User.objects.create_user(
            username='organiser',
            password='pass'
        )
        # creates 12 events to populate the view
        for i in range(12):
            Event.objects.create(
                event_name=f'Test Event{i}',
                event_date=timezone.now() + timezone.timedelta(days=3+i),
                created_on=timezone.now(),
                image='test.jpg',
                event_organiser=self.organiser,
                is_online=True,
                maximum_attendees=100,
                short_description='Short description',
                long_description='Long description',
            )
        self.own_event = Event.objects.create(
            event_name='Test Event for user',
            event_date=timezone.now() + timezone.timedelta(days=3),
            created_on=timezone.now(),
            image='test.jpg',
            event_organiser=self.user,
            is_online=True,
            maximum_attendees=100,
            short_description='Short description',
            long_description='Long description',
        )
        self.url = reverse('all-events')

    def test_redirects_if_not_logged_in(self):
        """
        Does not log the user in and attempts to get all events view. Should
        redirect to the index page and provide a message advising user can't
        view events unless they're logged in.
        """
        not_logged_in_error = (
            'You can not view events until you are logged in. '
            'Please sign up for an account or log in using the log in page.'
        )
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            not_logged_in_error,
            [m.message for m in messages]
        )

    def test_shows_only_future_events_not_created_by_user(self):
        """
        Logs the user in, then calls the list of all events and checks
        that the user's own events aren't included in the context. Also
        checks that all events are in the future.
        """
        self.client.login(username='test', password='pass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/all-events.html')
        events = response.context['events']
        for event in events:
            self.assertNotEqual(event.event_organiser, self.user)
            self.assertGreaterEqual(event.event_date, timezone.now())

    def test_pagination(self):
        """
        Tests that the pagination works for the list of events. Logs the
        user in and then navigates to the event page, checks that page 1
        only has 9 events, and that it has an option to go to the next page.
        Checks the next page has less than 9 events (only 12 are generated)
        and that there's an option to go back to the previous page.
        """
        self.client.login(username='test', password='pass')
        response = self.client.get(self.url)
        events_page_1 = response.context['events']
        self.assertEqual(len(events_page_1), 9)
        self.assertTrue(events_page_1.has_next())
        response = self.client.get(self.url + '?page=2')
        events_page_2 = response.context['events']
        self.assertLessEqual(len(events_page_2), 9)
        self.assertTrue(events_page_2.has_previous())


class TestSearchEventsView(TestCase):
    """
    TestCase for the search_events View.
    """

    def setUp(self):
        self.url = reverse('search-events')
        self.user = User.objects.create_user(
            username='test',
            password='pass'
        )
        for i in range(4):
            Event.objects.create(
                event_name=f'Test Event{i}',
                event_date=timezone.now() + timezone.timedelta(days=3+i),
                created_on=timezone.now(),
                image='test.jpg',
                event_organiser=self.user,
                is_online=True,
                maximum_attendees=100,
                short_description='Short description',
                long_description='Long description',
            )
        for i in range(3):
            Event.objects.create(
                event_name=f'Test Event{i}',
                event_date=timezone.now() - timezone.timedelta(days=3+i),
                created_on=timezone.now(),
                image='test.jpg',
                event_organiser=self.user,
                is_online=True,
                maximum_attendees=100,
                short_description='Short description',
                long_description='Long description',
            )

    def test_default_excludes_past_events(self):
        """
        Checks that the search query goes through, uses the correct template
        and does not include past events.
        """
        response = self.client.get(self.url, {'q': 'Event'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/search-events.html')
        self.assertEqual(response.context['results'].paginator.count, 4)
        self.assertFalse(response.context['include_past'])

    def test_includes_past_events_when_checked(self):
        """
        Checks that the search query goes through and includes past events.
        """
        response = self.client.get(
            self.url, {'q': 'Event', 'past-events': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['results'].paginator.count, 7)
        self.assertTrue(response.context['include_past'])

    def test_no_matching_results(self):
        """
        Tests that a query with non-matching results goes through but returns
        no results.
        """
        response = self.client.get(self.url, {'q': 'Nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nonexistent')
        self.assertEqual(response.context['results'].paginator.count, 0)

    def test_case_insensitive_search(self):
        """
        Tests that search results are case-insensitive.
        """
        response = self.client.get(self.url, {'q': 'Test Event'})
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.context['results'].paginator.count, 4)

    def test_pagination_limit(self):
        """
        Tests that pagination works correctly, that it paginates to 6
        events per page, that the second page request goes through, and that
        the second page has a previous page to navigate back to.
        """
        # Create 10 future events to force pagination
        for i in range(10):
            Event.objects.create(
                event_name=f'Extra Event {i}',
                event_date=timezone.now() + timezone.timedelta(days=i+10),
                created_on=timezone.now(),
                event_organiser=self.user,
                image='test.jpg',
                is_online=True,
                maximum_attendees=50,
                short_description='Extra description',
                long_description='Extra long description',
            )
        response = self.client.get(self.url, {'q': 'Event'})
        self.assertEqual(response.context['results'].paginator.num_pages, 3)
        self.assertEqual(len(response.context['results']), 6)
        response_page_2 = self.client.get(self.url, {'q': 'Event', 'page': 2})
        self.assertEqual(response_page_2.status_code, 200)
        self.assertTrue(response_page_2.context['results'].has_previous())


class TestBookingTicketsView(TestCase):
    """
    TestCase for the booking_events View.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='pass'
        )
        self.other_user = User.objects.create_user(
            username='other',
            password='pass'
        )
        self.event = Event.objects.create(
            event_name='Test Event',
            event_date=timezone.now() + timezone.timedelta(days=3),
            created_on=timezone.now(),
            image='test.jpg',
            event_organiser=self.other_user,
            is_online=True,
            maximum_attendees=100,
            short_description='Short description',
            long_description='Long description',
        )
        self.url = reverse('book-event', args=[self.event.id])

    def test_redirect_if_not_logged_in(self):
        """
        Tests that unauthenticated users are redirected to the index page,
        and that they receive a message explaining they can't book tickets.
        """
        not_logged_in_error = (
            'You cannot book tickets as you are not currently logged in. '
            'Please make an account using the sign up process, or log in.'
        )
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            not_logged_in_error,
            [m.message for m in messages]
        )

    def test_get_request_renders_form_for_logged_in_user(self):
        """
        Logs the user in and checks that a GET request for the view shows for
        a logged in user, that it calls the right template, and that the form
        and event are passed to the view from the context.
        """
        self.client.login(username='test', password='pass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/book-event.html')
        self.assertIn('form', response.context)
        self.assertIn('event', response.context)

    def test_post_valid_booking_creates_booking(self):
        """
        Logs the user in and checks that the user can post a request to book
        2 tickets for the event. Checks that the page redirects to the
        event-detail page, confirms that the event now has a booking,
        and that the booking characteristics match. Also confirms the user
        received a message about the booking going through.
        """
        self.client.login(username='test', password='pass')
        response = self.client.post(self.url, {
            'tickets': 2,
        }, follow=True)
        self.assertRedirects(response, reverse(
            'event-detail', args=[self.event.id]))
        self.assertEqual(Booking.objects.count(), 1)
        booking = Booking.objects.first()
        self.assertEqual(booking.event, self.event)
        self.assertEqual(booking.ticketholder, self.user)
        self.assertEqual(booking.tickets, 2)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            'Congratulations, your tickets are now booked.',
            [m.message for m in messages]
        )

    def test_post_invalid_data_does_not_create_booking(self):
        """
        Logs the user in, attempts to post a form without valid data. Checks
        that the post method does not go through, that a booking is not created
        and that the user is redirected to the same page with an error stating
        the field is required for the tickets field.
        """
        self.client.login(username='test', password='pass')
        response = self.client.post(self.url, {}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 0)
        self.assertTemplateUsed(response, 'events/book-event.html')
        form = response.context['form']
        self.assertFormError(form, 'tickets', 'This field is required.')

    def test_404_for_invalid_event_id(self):
        """
        Tests that a call for an invalid URL for an event returns a 404.
        """
        self.client.login(username='test', password='pass')
        bad_url = reverse('book-event', args=[999])
        response = self.client.get(bad_url)
        self.assertEqual(response.status_code, 404)

    def test_user_cannot_book_own_event(self):
        """
        Tests that a user cannot book tickets for an event they created
        themselves. Should redirect the user back to the book-event page
        and create a message advising they cannot book their own event.
        """
        self.client.login(username='other', password='pass')
        response = self.client.post(self.url, {'ticket': 1}, follow=True)
        self.assertEqual(Booking.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            "You cannot book your own event.",
            [m.message for m in messages]
        )

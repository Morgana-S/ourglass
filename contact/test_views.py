from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from .models import Message  # Adjust path if needed
# Create your tests here.


class TestMessageView(TestCase):
    """
    TestCase for message View.
    """

    def setUp(self):
        self.url = reverse('contact')
        self.user = User.objects.create_user(
            username='test', email='test@example.com', password='pass'
        )

    def test_get_request_renders_form(self):
        """
        Tests that a get request for the form returns the right status code,
        uses the right template, and passes the form correctly to the context.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')
        self.assertIn('form', response.context)

    def test_post_valid_message_anonymous_user(self):
        """
        Posts a form as an anonymous user, then checks that the post request
        goes through, that there is now a message object, and that the
        information in the message is correct. Also checks that the user
        receives confirmation that a message was sent.
        """
        success_message = (
            'Thank you, your message has been received and we will be '
            'in contact.'
        )
        form_data = {
            'guest_name': 'Jane Doe',
            'guest_email': 'jane@example.com',
            'message_reason': 'Other',
            'content': 'This is a message from a guest.'
        }
        response = self.client.post(self.url, data=form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Message.objects.count(), 1)
        msg = Message.objects.first()
        self.assertIsNone(msg.message_author)
        self.assertEqual(msg.guest_name, 'Jane Doe')
        self.assertEqual(msg.guest_email, 'jane@example.com')
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            success_message,
            [m.message for m in messages]
        )

    def test_post_valid_authenticated_user_creates_message(self):
        """
        Logs a user in, then populates the form with valid message data
        and attempts to post it. Confirms the status, that there is a new
        message, that the message_author is the user, their name is the 
        user's username, the email is the user's email address, and the
        message reason is the same as in the form.
        """
        self.client.login(username='test', password='pass')
        form_data = {
            'message_reason': 'Account',
            'content': 'I need help with my account.'
        }
        response = self.client.post(self.url, form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Message.objects.count(), 1)
        message = Message.objects.first()
        self.assertEqual(message.message_author, self.user)
        self.assertEqual(message.guest_name, self.user.username)
        self.assertEqual(message.guest_email, self.user.email)
        self.assertEqual(message.message_reason, 'Account')

    def test_post_missing_required_fields_anonymous_user(self):
        """
        Submits invalid data by not providing a guest_name or guest_email
        as an anonymous user. Confirms that the form does not submit and that
        the user is notified the form fields are required.
        """
        form_data = {
            'message_reason': 'Moderation',
            'content': 'Something went wrong'
        }
        response = self.client.post(self.url, form_data, follow=True)
        form = response.context['form']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Message.objects.count(), 0)
        self.assertFormError(form, 'guest_name',
                             'This field is required.')
        self.assertFormError(form, 'guest_email',
                             'This field is required.')

    def test_post_missing_content_authenticated_user(self):
        """
        Logs the user in, and tries to submit a form without a content message.
        Checks that the form is not submitted and that the user is informed
        the form field for content is required.
        """
        self.client.login(username='test', password='pass')
        form_data = {
            'message_reason': 'Tickets',
            'content': ''
        }
        response = self.client.post(self.url, form_data, follow=True)
        form = response.context['form']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Message.objects.count(), 0)
        self.assertFormError(form, 'content',
                             'This field is required.')

    def test_authenticated_display_name_and_email_address_properties(self):
        """
        Logs the user in, sends a form and then checks that the display_name
        and email address properties are properly filled.
        """
        self.client.login(username='test', password='pass')
        form_data = {
            'message_reason': 'Account',
            'content': 'Authenticated user test'
        }
        self.client.post(self.url, form_data)
        msg = Message.objects.first()
        self.assertEqual(str(msg.display_name), self.user.username)
        self.assertEqual(msg.email_address, self.user.email)

    def test_anonymous_display_name_and_email_address_properties(self):
        """
        Does not log the user in, sends a form, and then checks that the
        display_name and email address properties are properly filled.
        """
        form_data = {
            'guest_name': 'Guest User',
            'guest_email': 'guest@example.com',
            'message_reason': 'Other',
            'content': 'This is a message from an anonymous user.'
        }
        response = self.client.post(self.url, form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        msg = Message.objects.first()
        self.assertEqual(msg.display_name, 'Guest User')
        self.assertEqual(msg.email_address, 'guest@example.com')

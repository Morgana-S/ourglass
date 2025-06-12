from django import forms
from django.contrib.auth.models import User
from django.test import TestCase
from .forms import MessageForm
# Create your tests here.


class TestMessageForm(TestCase):
    """
    TestCase for all MessageForm tests.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@testemail.com'
        )
        self.valid_data = {
            'guest_name': 'Test User',
            'guest_email': 'testuser@testemail.com',
            'message_reason': 'Other',
            'content': 'This is a test message'
        }

    def test_valid_form_anonymous_user(self):
        """
        Tests whether the form is valid with all fields for anonymous
        users.
        """
        form = MessageForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), msg='form is invalid')

    def test_valid_form_authenticated_user(self):
        """
        Tests if the form is valid for authenticated users.
        """
        form = MessageForm(
            data={
                'message_reason': 'Other',
                'content': 'Authenticated user message'
            },
            user=self.user
        )
        self.assertTrue(form.is_valid(), msg='form is not valid')
        self.assertFalse(form.fields['guest_name'].required)
        self.assertFalse(form.fields['guest_email'].required)
        self.assertIsInstance(
            form.fields['guest_name'].widget, forms.HiddenInput)
        self.assertIsInstance(
            form.fields['guest_email'].widget, forms.HiddenInput)

    def test_invalid_form_missing_required_fields(self):
        """
        Tests if data is missing from required fields for anonymous users.
        """
        form = MessageForm(
            data={
                'message_reason': '',
                'content': ''
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('guest_name', form.errors)
        self.assertIn('guest_email', form.errors)
        self.assertIn('content', form.errors)

    def test_form_fields_hidden_for_authenticated_users(self):
        """
        Tests that the guest_name and guest_email form fields are hidden
        for authenticated users.
        """
        form = MessageForm(user=self.user)
        self.assertIsInstance(
            form.fields['guest_name'].widget, forms.HiddenInput)
        self.assertIsInstance(
            form.fields['guest_email'].widget, forms.HiddenInput)

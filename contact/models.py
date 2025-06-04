from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Message (models.Model):
    message_author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages',
    )
    guest_name = models.CharField(
        max_length=100,
        blank=True,
    )
    guest_email = models.EmailField(
        null=True,
    )
    MESSAGE_REASON_CHOICES = {
        'Account': 'Account Issues',
        'Business': 'Business Inquiry',
        'Moderation': 'Issues with another user',
        'Event Organisation': 'Event organisation issues',
        'Tickets': 'Booking / Ticket issues',
        'Other': 'Not Specified / Other'
    }
    message_reason = models.CharField(
        choices=MESSAGE_REASON_CHOICES,
        default='Other',
    )

    content = models.TextField(
        max_length=2000,
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    @property
    def display_name(self):
        if self.message_author:
            return self.message_author
        else:
            return self.guest_name

    @property
    def email_address(self):
        if self.message_author:
            return self.message_author.email
        else:
            return self.guest_email

    def __str__(self):
        return f'{self.display_name}: {self.message_reason}'

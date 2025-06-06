from django.contrib import admin
from .models import Message
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.


@admin.register(Message)
class MessageAdmin(SummernoteModelAdmin):
    list_display = ('id', 'message_author', 'guest_name',
                    'message_reason', 'email_address', 'created_on',)
    search_fields = ['message_author', 'guest_name', 'message_reason']
    list_filter = ('message_author', 'guest_name',
                   'message_reason', 'created_on',)

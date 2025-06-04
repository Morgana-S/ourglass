from .models import Message
from django import forms


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['guest_name', 'guest_email', 'message_reason', 'content']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            self.fields['guest_name'].widget = forms.HiddenInput()
            self.fields['guest_name'].required = False
            self.fields['guest_email'].widget = forms.HiddenInput()
            self.fields['guest_email'].required = False

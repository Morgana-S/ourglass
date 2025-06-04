from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Message
from .forms import MessageForm
# Create your views here.


def message_view(request):
    success_message = (
        "Thank you, your message has been received and we will be in contact."
    )
    if request.method == 'POST':
        message_form = MessageForm(request.POST, user=request.user)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            if request.user.is_authenticated:
                message.message_author = request.user
                message.guest_name = request.user.username
                message.guest_email = request.user.email
            message.save()
            messages.success(
                request,
                success_message
            )
            return redirect('contact')
    else:
        message_form = MessageForm(user=request.user)

    return render(request, 'contact/contact.html', {'form': message_form})

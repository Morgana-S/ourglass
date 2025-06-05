from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.timezone import now
from django.views import generic
from .models import Event, Booking
from .forms import EventForm
# Create your views here.


class LatestEventList(generic.ListView):
    """
    Returns a list of all event objects, ordered by the latest created.
    """
    queryset = Event.objects.all().order_by('-created_on')[:5]
    template_name = 'events/index.html'


class MyEventsDashboardView(LoginRequiredMixin, generic.TemplateView):
    """
    Returns all bookings that the user has tickets for, as well as all
    events the user has organised in one view.
    Also returns bookings that were previously attended to incentivize the
    user to leave a review.

    **Context**
    ``bookings``
        All booking objects that belong to the user logged in
        while on the page, excluding past events.

    ``organised_events``
        All event objects that were created by the logged in user.

    ``previous_bookings``
        All booking objects that belong to the user logged in
        while on the page, but only past events.

    **Template:**
    :template:`events/my-events.html`

    """

    template_name = 'events/my-events.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['bookings'] = Booking.objects.filter(
            ticketholder=user
        ).exclude(
            event__event_date__lt=now()
        )
        context['organised_events'] = Event.objects.filter(
            event_organiser=user
        ).exclude(
            event_date__lt=now()
        )
        context['previous_bookings'] = Booking.objects.filter(
            ticketholder=user,
            event__event_date__lt=now(),
        ).exclude(
            event__event_organiser=user
        )

        return context


def event_detail_view(request, event_id):
    """
    Returns a render for an individual event.
    """
    queryset = Event.objects.all()
    event = get_object_or_404(queryset, id=event_id)

    return render(
        request,
        'events/event-detail.html',
        {'event': event},
    )


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')


def create_event_view(request):
    success_message = (
        'Congratulations, your event has now been created '
        + 'and will now show up in your My Events Page.'
    )
    if request.method == 'POST':
        event_form = EventForm(request.POST, request.FILES)
        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.event_organiser = request.user
            event.save()
            messages.success(
                request,
                success_message
            )
            return redirect('my-events')
    else:
        event_form = EventForm()

    return render(request, 'events/create-event.html', {'form': event_form})


def edit_event_view(request, event_id):
    success_message = 'Your event has now been updated.'
    error_message = 'Your event was not updated successfully.'
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event_form = EventForm(data=request.POST, instance=event)
        if event_form.is_valid() and event.event_organiser == request.user:
            event = event_form.save()
            messages.success(request, success_message)
            return redirect('event-detail', event_id=event.id)
        else:
            messages.error(request, error_message)
    else:
        event_form = EventForm(instance=event)

    context = {
        'form': event_form,
        'event': event,
    }
    return render(request, 'events/edit-event.html', context)

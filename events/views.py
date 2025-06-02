from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render,get_object_or_404
from django.utils.timezone import now
from django.views import generic
from .models import Event, Booking
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
    messages.success(request, "You have been logged out.")
    return redirect('index')
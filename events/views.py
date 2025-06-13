from django.contrib import messages
from django.contrib.auth import logout, mixins
from django.core.paginator import Paginator
from django.db.models import (
    OuterRef, Exists, Q, Case, When, BooleanField, Value
)
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.timezone import now
from django.views import generic
from .models import Event, Booking, Review
from .forms import EventForm, ReviewForm, BookingForm
# Create your views here.


class LatestEventList(generic.ListView):
    """
    Returns a list of all event objects, ordered by the latest created.
    """
    queryset = Event.objects.all().order_by('-created_on')[:5]
    template_name = 'events/index.html'


class MyEventsDashboardView(mixins.LoginRequiredMixin, generic.TemplateView):
    """
    Returns all bookings that the user has tickets for, as well as all
    events the user has organised in one view.
    Also returns bookings that were previously attended to incentivize the
    user to leave a review.

    **Context**
    ``bookings``
        The paginated list of bookings provided by the bookings_qs queryset,
        ordered by event date.

    ``organised_events``
        The paginated list of organised events provided by the
        organised_events_qs queryset, ordered by event date.

    ``previous_bookings``
        The paginated list of previous bookings provided by the
        previous_bookings_qs queryset, ordered by event date.

    **Template**
    :template:`events/my-events.html`

    """

    template_name = 'events/my-events.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        reviews = Review.objects.filter(
            author=user,
            event=OuterRef('event')
        )
        bookings_qs = Booking.objects.filter(
            ticketholder=user
        ).exclude(
            event__event_date__lt=now()
        ).order_by(
            'event__event_date'
        )
        organised_events_qs = Event.objects.filter(
            event_organiser=user
        ).exclude(
            event_date__lt=now()
        ).order_by(
            'event_date'
        )
        previous_bookings_qs = Booking.objects.filter(
            ticketholder=user,
            event__event_date__lt=now(),
        ).annotate(
            has_review=Exists(reviews)
        ).order_by(
            'event__event_date'
        )

        # Pagination
        bookings_page_number = self.request.GET.get('bookings_page', 1)
        organised_events_page_number = self.request.GET.get(
            'organised_events_page',
            1
        )
        previous_bookings_page_number = self.request.GET.get(
            'previous_bookings_page',
            1
        )

        bookings_paginator = Paginator(bookings_qs, 6)
        organised_events_paginator = Paginator(organised_events_qs, 6)
        previous_bookings_paginator = Paginator(previous_bookings_qs, 6)

        context['bookings'] = bookings_paginator.get_page(bookings_page_number)
        context['organised_events'] = organised_events_paginator.get_page(
            organised_events_page_number
        )
        context['previous_bookings'] = previous_bookings_paginator.get_page(
            previous_bookings_page_number
        )

        return context


def event_detail_view(request, event_id):
    """
    Returns a render for an individual event, as well as providing information
    about the event's bookings and reviews.

    **Context**
    ``event``
        The event object for the page, determined by the id.

    ``user_has_booking``
        Checks whether the user has a booking for the event. Returns True
        if the user has a booking, and False if they don't.

    ``user_tickets``
        If the user has a booking, determined by the user_has_booking property,
        this allows access to the user's tickets value.

    ``user_has_reviewed``
        Checks if the user has left a review for this event.

    ``reviews``
        All reviews for the event, paginated using the Paginator.

    ``past_event``
        Checks if the event is in the past. Returns True if it is, False
        if it isn't.

    **Template**
    :template:`events/event-detail.html`


    """
    queryset = Event.objects.all()
    event = get_object_or_404(queryset, id=event_id)
    reviews = event.reviews.all()
    paginator = Paginator(reviews, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user_has_booking = False
    user_tickets = None
    if request.user.is_authenticated:
        user_booking = event.bookings.filter(ticketholder=request.user).first()
        if user_booking:
            user_has_booking = True
            user_tickets = user_booking.tickets
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = event.reviews.filter(
            author=request.user
        ).exists
    has_event_passed = event.event_date < now()
    context = {
        'event': event,
        'user_has_booking': user_has_booking,
        'user_tickets': user_tickets,
        'user_has_reviewed': user_has_reviewed,
        'reviews': page_obj,
        'past_event': has_event_passed,
    }
    return render(
        request,
        'events/event-detail.html',
        context,
    )


def logout_view(request):
    """
    Logs the user out of their account.
    """
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')


def create_event_view(request):
    """
    View for creating events. Passes the EventForm to the template and saves
    the user's inputs to the database as a new event.

    **Context**
    ``form``
        The form for the Event Model.

    **Template**
    :template:`events/create-event.html`
    """
    success_message = (
        'Congratulations, your event has now been created '
        + 'and will now show up in your My Events Page.'
    )
    error_message = (
        'Your event was not created. Please check the form fields and '
        'ensure all of the details are valid.'
    )
    not_logged_in_error = (
        'You cannot create an event as you are not currently logged in. '
        'Please make an account using the sign up process, or log in.'
    )

    if request.user.is_authenticated:
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
                messages.error(
                    request,
                    error_message
                )
        else:
            event_form = EventForm()
    else:
        messages.error(
            request,
            not_logged_in_error
        )
        return redirect('index')

    return render(request, 'events/create-event.html', {'form': event_form})


def edit_event_view(request, event_id):
    """
    View for editing events. Passes the EventForm prepopulated with the Event
    instance details, then saves changes to the event instance in the database.

    **Context**
    ``form``
        The form for the event model.

    ``event``
        The event that is being edited.

    **Template**
    :template:`events/edit-event.html`
    """
    success_message = 'Your event has now been updated.'
    error_message = 'Your event was not updated successfully.'
    not_logged_in_error = (
        'You cannot edit an event as you are not currently logged in. '
        'Please make an account using the sign up process, or log in.'
    )
    event = get_object_or_404(Event, id=event_id)

    if request.user.is_authenticated:
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
    else:
        messages.error(
            request,
            not_logged_in_error
        )
        return redirect('index')

    context = {
        'form': event_form,
        'event': event,
    }
    return render(request, 'events/edit-event.html', context)


def delete_event_view(request, event_id):
    """
    View for deleting events, accessed directly from the Edit Event template.
    Validation exists to ensure that the request.user is the event organiser.
    """
    event = get_object_or_404(Event, id=event_id)
    not_authorised_error = (
        'You do not have permission to delete this event.'
    )
    success_message = ('This event has now been deleted.')
    not_logged_in_error = (
        'You cannot delete an event as you are not currently logged in. '
        'Please make an account using the sign up process, or log in.'
    )
    if request.user.is_authenticated:
        if request.user != event.event_organiser:
            messages.error(request, not_authorised_error)
            return redirect('event-detail', event_id=event_id)
        else:
            event.delete()
            messages.success(request, success_message)
            return redirect('my-events')
    else:
        messages.error(
            request,
            not_logged_in_error
        )
        return redirect('index')


def review_event_view(request, event_id):
    """
    View for creating a review for an event. Passes the ReviewForm to the
    template and saves the users inputs, after adding information about
    the user and event, to the database as a new Review.

    **Context**
    ``event``
        The Event that is being reviewed.

    ``form``
        The form for the review model.

    **Template**
    :template:`events/review-event.html`
    """
    success_message = (
        'Thank you, your review has now been sent to our team '
        'for approval.'
    )
    ineligible_reviewer_error = (
        'Sorry, you cannot leave a review for this event.  '
        'This may be because you have already left a review, or '
        'you did not attend this event.'
    )
    not_logged_in_error = (
        'You cannot review an event as you are not currently logged in. '
        'Please make an account using the sign up process, or log in.'
    )
    error_message = ("Sorry, your review wasn't able to be submitted")
    event = get_object_or_404(Event, id=event_id)
    user_has_booking = False
    if request.user.is_authenticated:
        user_has_booking = event.bookings.filter(
            ticketholder=request.user
        ).exists()
        user_has_reviewed_event = event.reviews.filter(
            author=request.user
        ).exists()
        eligible_reviewer = user_has_booking and not user_has_reviewed_event
        if request.method == 'POST':
            review_form = ReviewForm(request.POST)
            if review_form.is_valid() and eligible_reviewer:
                review = review_form.save(commit=False)
                review.event = event
                review.author = request.user
                review.approved = False
                review.save()
                messages.success(request, success_message)
                return redirect('event-detail', event_id=event.id)
            elif not eligible_reviewer:
                messages.error(request, ineligible_reviewer_error)
                return redirect('event-detail', event_id=event.id)
            else:
                messages.error(request, error_message)
        else:
            review_form = ReviewForm(instance=event)
    else:
        messages.error(
            request,
            not_logged_in_error
        )
        return redirect('index')

    context = {
        'event': event,
        'form': review_form
    }
    return render(request, 'events/review-event.html', context)


def edit_review_view(request, review_id):
    """
    View for editing a review. Passes the ReviewForm prepopulated with the
    review instance details, then saves changes to the review in the database.

    **Context**
    ``form``
        The form for the Review Model.

    ``event``
        The instance of the event being reviewed.

    ``review``
        The instance of the review being edited.

    **Template**
    :template:`events/edit-review.html`
    """
    review = get_object_or_404(Review, id=review_id)
    event = get_object_or_404(Event, id=review.event.id)
    success_message = ('Your updated review is now awaiting approval.')
    error_message = ('Review was unable to be updated.')
    not_logged_in_error = (
        'You cannot edit a review as you are not currently logged in. '
        'Please make an account using the sign up process, or log in.'
    )

    if request.user.is_authenticated:
        if request.method == 'POST':
            review_form = ReviewForm(data=request.POST, instance=review)
            if review_form.is_valid() and review.author == request.user:
                review = review_form.save(commit=False)
                review.approved = False
                review.save()
                messages.success(request, success_message)
                return redirect('event-detail', event_id=event.id)
            else:
                messages.error(request, error_message)
                return redirect('event-detail', event_id=event.id)
        else:
            review_form = ReviewForm(instance=review)
    else:
        messages.error(
            request,
            not_logged_in_error
        )
        return redirect('index')

    context = {
        'form': review_form,
        'event': event,
        'review': review,
    }

    return render(request, 'events/edit-review.html', context)


def delete_review_view(request, review_id):
    """
    View for deleting reviews. Accessed through the edit-review template.
    Validation exists to ensure that only the reviewer can delete their review.
    """
    review = get_object_or_404(Review, id=review_id)
    not_logged_in_error = (
        'You can not delete a review if you are not logged in.'
    )
    get_request_error = (
        'Invalid request type (GET). Please contact the site administrators '
        'if you are seeing this message.'
    )
    if request.user.is_authenticated:
        if request.method == 'POST':
            if review.author != request.user:
                messages.error(
                    request,
                    "You can not delete other people's reviews."
                )
                return redirect('event-detail', event_id=review.event.id)
            else:
                review.delete()
                messages.success(request, 'Your review has now been deleted.')
                return redirect('event-detail', event_id=review.event.id)
        else:
            messages.error(request, get_request_error)
            return redirect('index')
    else:
        messages.error(request, not_logged_in_error)
        return redirect('index')


def all_events_view(request):
    """
    View for viewing all events, used with the 'Book Events' link in
    the navbar. This displays all events that are in the future that the user
    is eligible to book.

    **Context**
     ``events``
        The paginated list of events.

    **Template**
    :template:`events/all-events.html`

    """
    not_logged_in_error = (
        'You can not view events until you are logged in. '
        'Please sign up for an account or log in using the log in page.'
    )
    if request.user.is_authenticated:
        events = Event.objects.exclude(
            event_organiser=request.user
        ).filter(
            event_date__gte=now()
        ).order_by(
            'event_date'
        )

        paginator = Paginator(events, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'events': page_obj,
        }
    else:
        messages.error(
            request,
            not_logged_in_error
        )
        return redirect('index')

    return render(request, 'events/all-events.html', context)


def search_events_view(request):
    """
    View for event search results. Obtains the query information from the
    input on the search bar, as well as whether the user wants to see past
    events. These are then paginated to 6 events per page.

    **Context**
    ``query``
        The user's query from the search bar input.

    ``results``
        The paginated results from the search query.

    ``include_past``
        A property that returns true if past events are included.

    **Template**
    :template:`events/search-events.html`
    """
    query = request.GET.get('q', '')
    include_past = request.GET.get('past-events') == 'on'

    events = Event.objects.filter(
        Q(event_name__icontains=query)
    ).order_by('event_date')

    if not include_past:
        events = events.filter(event_date__gte=now())

    events = events.annotate(
        is_past=Case(
            When(event_date__lt=now(), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        )
    )

    paginator = Paginator(events, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'query': query,
        'results': page_obj,
        'include_past': include_past
    }
    return render(request, 'events/search-events.html', context)


def booking_tickets_view(request, event_id):
    """
    View for booking tickets for an event. Passes the BookingForm to the
    template and saves the user input to a new booking instance in the
    database.

    **Context**
    ``event``
        The event that the booking is for.

    ``form``
        The form for the Booking Model. Most information is passed to the
        booking instance afterwards - users are only expected to select
        their ticket amount.
    """
    not_logged_in_error = (
        'You cannot book tickets as you are not currently logged in. '
        'Please make an account using the sign up process, or log in.'
    )
    event = get_object_or_404(Event, id=event_id)

    if request.user.is_authenticated:
        if event.event_organiser == request.user:
            messages.error(request, 'You cannot book your own event.')
            return redirect('event-detail', event_id=event.id)
        if request.method == 'POST':
            success_message = (
                'Congratulations, your tickets are now booked.'
            )
            booking_form = BookingForm(
                request.POST,
                event=event,
                user=request.user
            )
            if booking_form.is_valid():
                booking = booking_form.save(commit=False)
                booking.event = event
                booking.ticketholder = request.user
                booking.save()
                messages.success(request, success_message)
                return redirect('event-detail', event_id=event.id)
        else:
            booking_form = BookingForm(event=event, user=request.user)
    else:
        messages.error(
            request,
            not_logged_in_error
        )
        return redirect('index')

    context = {
        'event': event,
        'form': booking_form,
    }
    return render(request, 'events/book-event.html', context)


def edit_booking_view(request, event_id):
    """
    View for editing a booking. Passes the BookingForm preopulated with the
    booking instance details, then saves changes to the booking in the
    database.

    **Context**
    ``event``
        The event the booking is for.

    ``form``
        The form for the Booking model.

    ``booking``
        The instance of the booking.

    *Template**
    :template:`events/edit-booking.html`
    """
    success_message = 'Your booking has now been updated.'
    not_logged_in_error = (
        'You cannot edit a booking as you are not currently logged in. '
        'Please make an account using the sign up process, or log in.'
    )
    if request.user.is_authenticated:
        event = get_object_or_404(Event, id=event_id)
        booking = get_object_or_404(
            Booking,
            event=event,
            ticketholder=request.user
        )
        if request.method == 'POST':
            booking_form = BookingForm(
                request.POST,
                instance=booking,
                event=event,
                user=request.user
            )
            if booking_form.is_valid():
                booking_form.save()
                messages.success(request, success_message)
                return redirect('event-detail', event_id=event.id)
        else:
            booking_form = BookingForm(
                instance=booking,
                event=event,
                user=request.user
            )
    else:
        messages.error(
            request,
            not_logged_in_error
        )
        return redirect('index')

    context = {
        'event': event,
        'form': booking_form,
        'booking': booking,
    }
    return render(request, 'events/edit-booking.html', context)


def delete_booking_view(request, booking_id):
    """
    View for deleting bookings. Accessed through the edit-booking template.
    Validation exists to ensure that only the ticketholder can delete their
    bookings.
    """
    if request.user.is_authenticated:
        booking = get_object_or_404(Booking, id=booking_id)

        if booking.ticketholder != request.user:
            messages.error(
                request,
                "You can not cancel other people's bookings."
            )
            return redirect('event-detail', event_id=booking.event.id)
        else:
            booking.delete()
            messages.success(request, 'Your booking has now been cancelled.')
            return redirect('event-detail', event_id=booking.event.id)
    else:
        messages.error(request, 'You are not logged in.')
        return redirect('index')

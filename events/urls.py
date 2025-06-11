from . import views
from django.urls import path

urlpatterns = [
    path(
        'events/<int:event_id>/',
        views.event_detail_view,
        name='event-detail'
    ),
    path(
        'events/all-events/',
        views.all_events_view,
        name='all-events'
    ),
    path(
        'events/book-event/<int:event_id>/',
        views.booking_tickets_view,
        name='book-event'
    ),
    path(
        'events/edit-booking/<int:event_id>/',
        views.edit_booking_view,
        name='edit-booking'
    ),
    path(
        'events/edit-event/<int:event_id>/',
        views.edit_event_view,
        name='edit-event'
    ),
    path(
        'events/edit-review/<int:review_id>/',
        views.edit_review_view,
        name='edit-review'
    ),
    path('events/create-event/', views.create_event_view, name='create-event'),
    path(
        'events/delete-booking/<int:booking_id>/',
        views.delete_booking_view,
        name='delete-booking'
    ),
    path(
        'events/delete-event/<int:event_id>/',
        views.delete_event_view,
        name='delete-event'
    ),
    path(
        'events/delete-review/<int:review_id>/',
        views.delete_review_view,
        name='delete-review'
    ),
    path('events/review-event/<int:event_id>/',
         views.review_event_view,
         name='review-event'
         ),
    path('logout/', views.logout_view, name='logout'),
    path('myevents/', views.MyEventsDashboardView.as_view(), name='my-events'),
    path('search-events/', views.search_events_view, name='search-events'),
    path('', views.LatestEventList.as_view(), name='index'),
]

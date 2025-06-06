from . import views
from django.urls import path

urlpatterns = [
    path(
        'events/<int:event_id>/',
        views.event_detail_view,
        name='event-detail'
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
    path('events/create-event/', views.create_event_view, name='create-event'),
    path(
        'events/edit-event/<int:event_id>/',
        views.edit_event_view,
        name='edit-event'
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

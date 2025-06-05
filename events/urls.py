from . import views
from django.urls import path

urlpatterns = [
    path(
        'events/<int:event_id>/',
        views.event_detail_view,
        name='event-detail'
    ),
    path('events/create-event/', views.create_event_view, name='create-event'),
    path(
        'events/edit-event/<int:event_id>/',
        views.edit_event_view,
        name='edit-event'
    ),
    path('logout/', views.logout_view, name='logout'),
    path('myevents/', views.MyEventsDashboardView.as_view(), name='my-events'),
    path('', views.LatestEventList.as_view(), name='index'),
]

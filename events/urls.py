from . import views
from django.urls import path

urlpatterns = [
    path(
        'events/<int:event_id>/',
        views.event_detail_view,
        name='event-detail'
        ),
    path('logout/', views.logout_view, name='logout'),
    path('myevents/', views.MyEventsDashboardView.as_view(), name='my-events'),
    path('', views.LatestEventList.as_view(), name='index'),
]

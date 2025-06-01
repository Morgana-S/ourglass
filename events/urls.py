from . import views
from django.urls import path

urlpatterns = [
    path('', views.LatestEventList.as_view(), name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('myevents/', views.MyEventsDashboardView.as_view(), name='my-events'),
]

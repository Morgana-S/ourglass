from . import views
from django.urls import path

urlpatterns = [
    path('', views.LatestEventList.as_view(), name='index'),
]

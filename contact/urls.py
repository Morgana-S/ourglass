from . import views
from django.urls import path

urlpatterns = [
    path('', views.message_view, name='contact')
]

from django.urls import path
from . import views
from .. import settings

urlpatterns = [
    path('json/', views.events_json, name='events_json'),  # API за JSON събития
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('create/', views.create_event, name='create_event'),
    path('<int:pk>/', views.event_details, name='event_details'),
    path('<int:pk>/edit/', views.edit_event, name='edit_event'),
    path('<int:pk>/delete/', views.delete_event, name='delete_event'),
    path('<int:event_id>/invite/', views.invite_followers, name='invite_followers'),
    path('rsvp/<int:participant_id>/<str:response>/', views.rsvp, name='rsvp'),

]

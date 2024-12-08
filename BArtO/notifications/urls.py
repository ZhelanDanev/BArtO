from django.urls import path

from BArtO.notifications import views

urlpatterns = [
    path('', views.notifications_list, name='notifications_list'),
    path('mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('collaborate/<int:user_id>/', views.collaborate_with_user, name='collaborate_with_user'),
    path('chat/<int:user_id>/', views.chat_view, name='chat_view'),
]

from django.urls import path

from BArtO.common.views import custom_404, home, search_users

urlpatterns = [
    path('', home, name='home'),
    path('search/', search_users, name='search_users'),
]

handler404 = custom_404

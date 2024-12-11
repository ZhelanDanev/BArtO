from django.conf.urls import handler404
from django.contrib.auth import get_user_model
from django.shortcuts import render
from BArtO.notifications.models import Notification


def home(request):
    return render(request, 'common/home.html')


def homepage(request):
    unread_notifications_count = 0
    if request.user.is_authenticated:
        unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()

    return render(request, 'common/base.html', {
        'unread_notifications_count': unread_notifications_count,
    })


User = get_user_model()


def search_users(request):
    query = request.GET.get('q')
    users = User.objects.filter(username__icontains=query)
    return render(request, 'common/search_results.html', {'users': users})


def custom_404(request, exception):
    return render(request, 'common/404.html', status=404)


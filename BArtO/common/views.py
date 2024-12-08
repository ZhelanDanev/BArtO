from django.shortcuts import render
from BArtO.notifications.models import Notification


def homepage(request):
    unread_notifications_count = 0
    if request.user.is_authenticated:
        unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()

    return render(request, 'common/base.html', {
        'unread_notifications_count': unread_notifications_count,
    })

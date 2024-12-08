from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Notification


@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications,
    })


@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'success': True})

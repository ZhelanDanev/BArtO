from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Connection, Message
from .forms import CollaborationForm
from BArtO.accounts.models import AppUser, Artist
from ..notifications.models import Notification


@login_required
def follow_user(request, user_id):
    """Follow an artist."""
    artist = get_object_or_404(Artist, pk=user_id)
    if artist.user != request.user:
        # Създаваме връзка за следване
        connection, created = Connection.objects.get_or_create(
            from_user=request.user,
            to_user=artist.user,
            connection_type=Connection.FOLLOW,
        )

        # Създаваме уведомление за ново последване
        if created:
            notification_message = f"{request.user.username} is now following you!"
            Notification.objects.create(
                user=artist.user,
                message=notification_message,
                notification_type=Notification.FOLLOW,
                sender=request.user  # Добавяме ID на артиста в уведомлението
            )
    return redirect('artist_details', pk=user_id)



@login_required
def unfollow_user(request, user_id):
    """Unfollow an artist."""
    artist = get_object_or_404(Artist, pk=user_id)
    Connection.objects.filter(
        from_user=request.user,
        to_user=artist.user,
        connection_type=Connection.FOLLOW,
    ).delete()
    return redirect('artist_details', pk=user_id)


@login_required
def collaborate_with_user(request, user_id):
    """Handle collaboration requests."""
    to_user = get_object_or_404(AppUser, id=user_id)

    if request.method == "POST":
        form = CollaborationForm(request.POST)
        if form.is_valid():
            # Here, handle email sending or save the collaboration request in the database.
            # Example: Send email or save data.
            message = form.cleaned_data['message']
            print(f"Collaboration request sent to {to_user.email} with message: {message}")
            return JsonResponse({'message': 'Collaboration request sent successfully!'})
    else:
        form = CollaborationForm()

    return render(request, 'connection/collaborate.html', {'form': form, 'to_user': to_user})


UserModel = get_user_model()


@login_required
def chat_view(request, user_id):
    other_user = get_object_or_404(UserModel, id=user_id)
    messages = Message.objects.filter(
        (models.Q(sender=request.user, receiver=other_user) |
         models.Q(sender=other_user, receiver=request.user))
    ).order_by('timestamp')

    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=other_user, content=content)

    return render(request, 'connection/chat.html', {
        'messages': messages,
        'other_user': other_user,
    })

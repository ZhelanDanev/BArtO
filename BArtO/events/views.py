from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import EventForm, CommentForm
from .models import Event, EventParticipant, Comment
from ..accounts.models import AppUser
from ..connections.models import Connection
from ..notifications.models import Notification

UserModel = get_user_model()


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  # Задаваме организатора
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('calendar_view')  # Пренасочване към календара
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Create Event'})


@login_required
def event_details(request, pk):
    event = get_object_or_404(Event, pk=pk)
    is_organizer = event.organizer == request.user

    # Получаваме потвърдените гости
    confirmed_guests = EventParticipant.objects.filter(event=event, confirmed=True)
    confirmed_count = confirmed_guests.count()  # Броя на потвърдените гости

    # Проверка дали потребителят е поканен
    user_invited = EventParticipant.objects.filter(event=event, artist=request.user).exists()
    participant = None
    if user_invited:
        participant = EventParticipant.objects.get(event=event, artist=request.user)

    # Ако има заявка за потвърждение или отказ
    if request.method == 'POST' and participant:
        if 'accept_invitation' in request.POST:
            participant.confirmed = True
            participant.save()
            messages.success(request, "You have accepted the invitation!")
            return redirect('event_details', pk=event.pk)
        elif 'decline_invitation' in request.POST:
            participant.confirmed = False
            participant.save()
            messages.success(request, "You have declined the invitation.")
            return redirect('event_details', pk=event.pk)

    if request.method == 'POST' and 'submit_comment' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.event = event
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect('event_details', pk=event.pk)
    else:
        comment_form = CommentForm()

    comments = event.comments.all()  # Всички коментари към събитието

    # Другата логика за събитието
    context = {
        'event': event,
        'is_organizer': is_organizer,
        'confirmed_guests': confirmed_guests,
        'confirmed_count': confirmed_count,
        'user_invited': user_invited,
        'participant': participant,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'events/event_details.html', context)


@login_required
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.organizer != request.user:
        return redirect('event_details', pk=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_details', pk=pk)
    else:
        form = EventForm(instance=event)

    return render(request, 'events/edit_event.html', {'form': form})


@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.organizer != request.user:
        return redirect('event_details', pk=pk)

    if request.method == 'POST':
        event.delete()
        return redirect('calendar_view')

    return render(request, 'events/delete_event.html', {'event': event})


def event_participants(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = event.participants.filter(confirmed=True)
    return render(request, 'events/participants.html', {'event': event, 'participants': participants})


@login_required
def invite_followers(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if event.organizer != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    # Получаваме последователите на потребителя
    followers = Connection.objects.filter(from_user=request.user, connection_type=Connection.FOLLOW)
    follower_users = [connection.to_user for connection in followers]

    if request.method == 'POST':
        user_ids = request.POST.getlist('user_ids')  # Получаваме ID-та на избраните последователи
        for user_id in user_ids:
            follower_user = get_object_or_404(UserModel, pk=user_id)

            # Поканване на потребителя за събитието
            EventParticipant.objects.get_or_create(event=event, artist=follower_user)

            # Създаване на уведомление за поканата с ID на събитието
            notification_message = f"You have been invited to the event: {event.title}"
            Notification.objects.create(
                user=follower_user,
                message=notification_message,
                notification_type="event_invite",
                event_id=event.pk  # Добавяме ID на събитието в уведомлението
            )

        return JsonResponse({'message': 'Invitations sent successfully.'})

    return render(request, 'events/invite_followers.html', {'event': event, 'followers': follower_users})


def rsvp(request, participant_id, response):
    participant = get_object_or_404(EventParticipant, id=participant_id, artist=request.user)
    participant.confirmed = response
    participant.save()
    messages.success(request, "RSVP updated!")
    return redirect('event_detail', event_id=participant.event.id)


def events_json(request):
    events = Event.objects.all()
    event_list = [
        {
            "id": event.id,
            "title": event.title,
            "start": event.start_time.isoformat(),
            "end": event.end_time.isoformat() if event.end_time else None,
            "url": f"/events/{event.id}/",  # линк към детайлите на събитието
        }
        for event in events
    ]
    return JsonResponse(event_list, safe=False)


def calendar_view(request):
    return render(request, 'events/calendar.html')
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView


from .forms import ArtistEditForm, ArtistRegistrationForm
from .models import Artist, AppUser
from ..connections.models import Connection
from ..notifications.models import Notification


@login_required
def notification_list(request):
    # Вземаме всички уведомления за потребителя
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})


@login_required
def profile_details(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)

    # Вземете новите (непрочетени) нотификации
    new_notifications = Notification.objects.filter(user=request.user, is_read=False)

    context = {
        'artist': artist,
        'new_notifications_count': new_notifications.count(),
    }

    return render(request, 'profile/profile-details.html', context)


class ArtistRegisterView(CreateView):
    form_class = ArtistRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()

        artist = Artist.objects.create(
            user=user,
            first_name=form.cleaned_data.get('first_name'),
            last_name=form.cleaned_data.get('last_name'),
            category=form.cleaned_data.get('category'),
            profile_picture=form.cleaned_data.get('profile_picture'),
        )

        if artist.profile_picture:
            artist.save()

        login(self.request, user)
        return redirect('home')


class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'profile/profile-details.html'
    context_object_name = 'artist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artist = self.get_object()

        followers = Connection.objects.filter(
            to_user=artist.user,
            connection_type=Connection.FOLLOW
        )
        context['followers'] = followers

        following = Connection.objects.filter(
            from_user=artist.user,
            connection_type=Connection.FOLLOW
        )
        context['following'] = following

        if self.request.user.is_authenticated:
            context['is_following'] = followers.filter(from_user=self.request.user).exists()
        else:
            context['is_following'] = False

        # Проверка дали разглежданият профил принадлежи на текущия потребител
        context['is_own_profile'] = self.request.user == artist.user

        # Вземаме всички нотификации за текущия потребител
        if self.request.user.is_authenticated:
            notifications = Notification.objects.filter(user=self.request.user).order_by('-created_at')
            # Вземаме броя на непрочетените нотификации
            unread_notifications_count = Notification.objects.filter(user=self.request.user, is_read=False).count()
            context['unread_notifications_count'] = unread_notifications_count
            context['notifications'] = notifications

        return context


def artist_edit(request, pk):
    # Вземаме свързания Artist
    artist = getattr(request.user, 'artist', None)
    if not artist or artist.pk != pk:
        return redirect('artist_details', pk=pk)

    if request.method == 'POST':
        form = ArtistEditForm(request.POST, request.FILES, instance=artist, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профилът е успешно обновен!")
            return redirect('artist_details', pk=pk)
        else:
            messages.error(request, "Моля, коригирайте грешките във формуляра.")
    else:
        form = ArtistEditForm(instance=artist, user=request.user)

    return render(request, 'profile/profile-edit.html', {'artist_form': form})


class ArtistDeleteView(DeleteView):
    model = Artist
    success_url = reverse_lazy('home')  # Заменете с желания URL след изтриване
    template_name = 'profile/profile-delete.html'  # Шаблон за формата за потвърждение

    def get_object(self):
        try:
            return Artist.objects.get(user=self.request.user)
        except Artist.DoesNotExist:
            raise Http404("Профилът на артиста не съществува.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['artist'] = self.object  # Предаване на обекта на артиста в контекста
        return context


def logout_view(request):
    logout(request)
    return redirect('login')


def artist_list(request):
    query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')

    # Използваме Artist модела, за да получим всички свързани потребители
    artist_queryset = Artist.objects.all()

    if query:
        artist_queryset = artist_queryset.filter(user__username__icontains=query)

    if category_filter:
        artist_queryset = artist_queryset.filter(category=category_filter)

    return render(request, 'profile/artist_list.html', {
        'artists': artist_queryset,
        'query': query,
        'category_filter': category_filter
    })

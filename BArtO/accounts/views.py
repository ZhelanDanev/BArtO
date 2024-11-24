from django.contrib.auth import login, logout, get_user_model
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView

from .forms import ArtistEditForm, ArtistRegistrationForm
from .models import Artist


def home(request):
    return render(request, 'common/home.html')


class ArtistRegisterView(CreateView):
    form_class = ArtistRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Създаваме потребителя
        user = form.save()

        # Създаваме профила на артиста
        artist = Artist.objects.create(
            user=user,
            first_name=form.cleaned_data.get('first_name'),
            last_name=form.cleaned_data.get('last_name'),
            category=form.cleaned_data.get('category'),
            profile_picture=form.cleaned_data.get('profile_picture'),
        )

        # Ако има качена профилна снимка, я запазваме
        if artist.profile_picture:
            artist.save()

        login(self.request, user)
        return redirect('home')


class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'profile/profile-details.html'
    context_object_name = 'artist'

    def get_object(self, queryset=None):
        # Проверява дали потребителят има свързан профил
        if self.request.user.is_authenticated:
            try:
                return Artist.objects.get(user=self.request.user)
            except Artist.DoesNotExist:
                return redirect('register')  # Ако няма профил, пренасочва
        return redirect('login')  # Ако не е влязъл в системата


def artist_edit(request, pk):
    # Вземаме потребителя
    artist = getattr(request.user, 'artist', None)

    # Ако потребителят няма свързан Artist
    if not artist:
        return redirect('register')

    # Обработка на POST заявката
    if request.method == 'POST':
        artist_form = ArtistEditForm(request.POST, request.FILES, instance=artist)
        if artist_form.is_valid():
            artist_form.save()
            return redirect('artist_details', pk=pk)  # Пренасочваме към профила
    else:
        # Ако е GET заявка, зареждаме формата със съществуващите данни за artist
        artist_form = ArtistEditForm(instance=artist)

    return render(request, 'profile/profile-edit.html', {'artist_form': artist_form})


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

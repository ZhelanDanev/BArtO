
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Artist

UserModel = get_user_model()


class ArtistRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=True, label="First Name")
    last_name = forms.CharField(required=True, label="Last Name")
    category = forms.ChoiceField(
        choices=[('musician', 'Музикант'), ('writer', 'Писател'), ('actor', 'Актьор')],
        label="Категория",
        widget=forms.Select(attrs={'id': 'id_category'}),
    )

    # Линкове за социални медии
    facebook = forms.URLField(
        required=False,
        label="Facebook",
        widget=forms.TextInput(attrs={
            'placeholder': 'Въведете линк за Facebook профил',
            'class': 'form-control',
        })
    )

    youtube = forms.URLField(
        required=False,
        label="YouTube",
        widget=forms.TextInput(attrs={
            'placeholder': 'Въведете линк за YouTube профил',
            'class': 'form-control',
        })
    )

    instagram = forms.URLField(
        required=False,
        label="Instagram",
        widget=forms.TextInput(attrs={
            'placeholder': 'Въведете линк за Instagram профил',
            'class': 'form-control',
        })
    )

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'category', 'facebook',
                  'youtube', 'instagram']

    def save(self, commit=True):
        user = super().save(commit=False)

        # Записваме социалните медийни линкове
        user.social_media_links = {
            'facebook': self.cleaned_data.get('facebook'),
            'youtube': self.cleaned_data.get('youtube'),
            'instagram': self.cleaned_data.get('instagram'),
        }

        if commit:
            user.save()

        return user


# class ArtistEditForm(forms.ModelForm):
#     social_media_links = forms.CharField(
#         widget=forms.Textarea(attrs={'rows': 3}),
#         required=False, label="Social Media Links (JSON format)")
#
#     class Meta:
#         model = Artist
#         exclude = ['user']


class ArtistEditForm(forms.ModelForm):
    facebook = forms.URLField(
        required=False,
        label="Facebook",
        widget=forms.TextInput(attrs={
            'placeholder': 'Facebook линк',
            'class': 'form-control',
        })
    )
    youtube = forms.URLField(
        required=False,
        label="YouTube",
        widget=forms.TextInput(attrs={
            'placeholder': 'YouTube линк',
            'class': 'form-control',
        })
    )
    instagram = forms.URLField(
        required=False,
        label="Instagram",
        widget=forms.TextInput(attrs={
            'placeholder': 'Instagram линк',
            'class': 'form-control',
        })
    )

    class Meta:
        model = Artist
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Приемаме `user` като аргумент
        super().__init__(*args, **kwargs)
        if self.user and hasattr(self.user, 'social_media_links'):
            social_links = self.user.social_media_links or {}
            self.fields['facebook'].initial = social_links.get('facebook', '')
            self.fields['youtube'].initial = social_links.get('youtube', '')
            self.fields['instagram'].initial = social_links.get('instagram', '')

    def save(self, commit=True):
        artist = super().save(commit=False)
        if self.user:
            self.user.social_media_links = {
                'facebook': self.cleaned_data.get('facebook'),
                'youtube': self.cleaned_data.get('youtube'),
                'instagram': self.cleaned_data.get('instagram'),
            }
            if commit:
                self.user.save()
        if commit:
            artist.save()
        return artist

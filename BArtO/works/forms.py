from django import forms
from .models import Work

class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['title', 'category', 'genre', 'description', 'youtube_link', 'audio_file', 'text_content']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'text_content': forms.Textarea(attrs={'rows': 10}),
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        youtube_link = cleaned_data.get('youtube_link')
        audio_file = cleaned_data.get('audio_file')
        text_content = cleaned_data.get('text_content')

        if category == 'music' and not (youtube_link or audio_file):
            raise forms.ValidationError("Music must include a YouTube link or an audio file.")
        if category == 'writing' and not text_content:
            raise forms.ValidationError("Writing must include text content.")
        if category == 'acting' and not youtube_link:
            raise forms.ValidationError("Acting must include a YouTube link.")

        return cleaned_data

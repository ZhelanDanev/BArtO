from django import forms
from .models import Event, Comment


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'poster', 'description', 'start_time', 'end_time', 'location', 'discussion_enabled']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'discussion_enabled': 'Позволи дискусията за това събитие',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add your comment...'}),
        }

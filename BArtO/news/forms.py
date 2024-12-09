from django import forms
from .models import NewsComment, News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']

    def save(self, commit=True, user=None):
        news = super().save(commit=False)
        if user:
            news.author = user
        if commit:
            news.save()
        return news


class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}),
        }

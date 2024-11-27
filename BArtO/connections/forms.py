from django import forms


class CollaborationForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Представи ми кой си и защо искаш да направим колаборация...'}),
        max_length=1000,
        label="Message",
    )

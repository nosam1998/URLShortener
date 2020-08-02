from django import forms

from .models import ShortenedUrl


class CreateShortUrlForm(forms.ModelForm):
    class Meta:
        model = ShortenedUrl
        fields = ['original_url', 'slug']

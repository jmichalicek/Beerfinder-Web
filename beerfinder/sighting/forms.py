from django import forms

from .models import Sighting

class SightingModelForm(forms.ModelForm):

    class Meta:
        model = Sighting
        fields = ('user', 'image', 'comment', 'venue', 'beer')

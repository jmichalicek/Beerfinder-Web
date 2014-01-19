from django import forms

from .models import Sighting, SightingConfirmation

class SightingModelForm(forms.ModelForm):

    class Meta:
        model = Sighting
        fields = ('user', 'image', 'comment', 'venue', 'beer')

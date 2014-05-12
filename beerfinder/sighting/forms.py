from django import forms

from .models import Sighting, SightingConfirmation, SightingImage

class SightingModelForm(forms.ModelForm):

    class Meta:
        model = Sighting
        fields = ('user', 'comment', 'venue', 'beer', 'serving_types')

class SightingImageForm(forms.ModelForm):

    class Meta:
        model = SightingImage
        fields = ('original', 'user', 'sighting')

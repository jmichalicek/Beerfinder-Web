from django import forms

import re

from .models import Beer, Brewery


class AddBeerForm(forms.Form):
    """
    Form for adding a new beer.
    Used instead of DRF serializer because the odd validation
    required specifically for adding a beer is not desirable on the main
    Beer serializer
    """

    beer = forms.CharField(max_length=75)
    brewery = forms.CharField(max_length=75)

    def clean(self, *args, **kwargs):
        cleaned_data = super(AddBeerForm, self).clean(*args, **kwargs)
        beer_name = cleaned_data.get('beer', '')
        brewery_name = cleaned_data.get('brewery', '')

        if Beer.objects.filter(name=beer_name, brewery__name=brewery_name).exists():
            raise forms.ValidationError("This beer already exists")

        return cleaned_data

    def clean_beer(self):
        """
        strips whitespace off of both ends of the beer_name
        and condenses all whitespace to a single space.
        """
        beer_name = self.cleaned_data.get('beer', '')
        beer_name = re.sub(r'\s+', ' ', beer_name)
        return beer_name.strip()

    def clean_brewery(self):
        """
        strips whitespace off of both ends of the brewery_name
        and condenses all whitespace to a single space.
        """
        brewery_name = self.cleaned_data.get('brewery', '')
        brewery_name = re.sub(r'\s+', ' ', brewery_name)
        return brewery_name.strip()

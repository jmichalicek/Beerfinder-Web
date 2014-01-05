from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import JSONRenderer

from beer.models import Beer
from beer.serializers import BeerSerializer

from .models import Sighting
from .serializers import SightingSerializer

def sightings_near_user(request):
    """
    Display a list of sightings near the user's current location ordered by time.
    Actually does not do much since that will all be handled via ajax and so this basically
    just loads the correct template.
    """

    return render_to_response('sighting/nearby_sightings.html',
                              {},
                              context_instance=RequestContext(request))


@login_required
def add_sighting(request):
    beer_slug = request.GET.get('beer')
    beer = get_object_or_404(Beer, slug=beer_slug)

    serialized = BeerSerializer(beer)

    return render_to_response('sighting/add_sighting.html',
                              {'beer': JSONRenderer().render(serialized.data)},
                              context_instance=RequestContext(request))


def sighting_detail(request, sighting_id):
    sighting = get_object_or_404(Sighting.objects.select_related('beer', 'beer__brewery', 'venue'), id=sighting_id)
    serialized = SightingSerializer(sighting)

    return render_to_response('sighting/detail.html',
                              {'sighting': JSONRenderer().render(serialized.data)},
                              context_instance=RequestContext(request))

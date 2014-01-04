from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from rest_framework.renderers import JSONRenderer

from .models import Beer
from .serializers import BeerSerializer

def list_beer(request):
    return render_to_response('beer/list_beer.html',
                              {},
                              context_instance=RequestContext(request))


def beer_detail(request, beer_slug):
    # this seems kind of silly, this is just basically going to be done again by the api
    # the template could use this Beer object, but it will use the api for consistency
    beer = get_object_or_404(Beer, slug=beer_slug)

    serialized = BeerSerializer(beer)

    return render_to_response('beer/detail.html',
                              {'beer': JSONRenderer().render(serialized.data)},
                              context_instance=RequestContext(request))

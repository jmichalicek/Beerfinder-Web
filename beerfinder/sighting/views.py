from django.shortcuts import render_to_response
from django.template import RequestContext

def sightings_near_user(request):
    """
    Display a list of sightings near the user's current location ordered by time.
    Actually does not do much since that will all be handled via ajax and so this basically
    just loads the correct template.
    """

    return render_to_response('sighting/nearby_sightings.html',
                              {},
                              context_instance=RequestContext(request))

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import JSONRenderer


@login_required
def edit_profile(request):
    return render_to_response('accounts/edit_profile.html',
                              {},
                              context_instance=RequestContext(request))

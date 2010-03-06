from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from forms import ProfileForm
from models import Buddy

@login_required
def search(request):
    """
    On post, recieve a string and radius, geocode, and return a bunch of
    buddies within that radius
    """
    # prevent access by non-organisations
    try:
        organisation = request.user.organisation
    except AttributeError:
        return HttpResponseForbidden()
    
    buddies_in_range = []
    if request.method == 'POST':
        # geocode address
        lat, lng = magical_geocode_function(request.method.get('location'))
        # to keep things super simple, pull out all buddies, then filter in
        # memory. obviously this will have to be fixed once there is a
        # non-trivial number of buddies in the db. and when we have more 
        # than a day to work on this thing
        buddies = Buddy.objects.all()
        for buddy in buddies:
            buddy_lat, buddy_lng = buddy.location.latitude, buddy.location.longitude
            if (buddy_lat - lat) ** 2 + (buddy_lng - lng) ** 2 <= request.POST.get('range') ** 2:
                buddies_in_range.append(buddy)

    return render_to_response('buddies/search.html', {
        'buddies_in_range': buddies_in_range
    }, context_instance=RequestContext(request))

def profile(request, pk=None):
    """
    Create or edit a buddy profile
    """
    if pk:
        # if editing, ensure that it is the correct user
        if not pk == request.user.pk:
            return HttpResponseForbidden()
        instance = request.user.buddy
    else:
        instance = None
        
    form = ProfileForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Profile details have been updated')
        return redirect('.')

    return render_to_response('buddies/profile.html', {
        'buddy': instance,
        'form': form
    }, context_instance=RequestContext(request))

@login_required
def detail(request, pk):
    """
    View a buddy profile
    """
    buddy = get_object_or_404(Buddy, pk=pk)
    # if not viewing own profile, restrict to organisations
    if not request.user.pk == pk:
        try:
            organisation = request.user.organisation
        except AttributeError:
            return HttpResponseForbidden()

    return render_to_response('buddies/detail.html', {
        'buddy': buddy
    }, context_instance=RequestContext(request))
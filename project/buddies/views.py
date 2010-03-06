from urllib import urlencode
from urllib2 import urlopen
import simplejson

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string

from forms import ProfileForm, SearchForm, MessageForm, MessageResponseForm
from models import Buddy, ContactLog

from library.geo import points2distance

GEOCODER_URL = 'http://maps.google.com/maps/geo?q=%s&output=json&sensor=false&key=' + settings.GOOGLE_MAPS_API_KEY    

def geocode(location_str):
    result = urlopen(GEOCODER_URL % urlencode({'q': location_str}))
    data = simplejson.loads(result.read())
    if not data['Status']['code'] == 200:
        pass #handle error
    lng, lat, _ = data['Placemark'][0]['Point']['coordinates']
    return float(lat), float(lng)

@login_required
def search(request):
    """
    On post, recieve a string and radius, geocode, and return a bunch of
    buddies within that radius
    """
    # prevent access by non-organisations
    try:
        organisation = request.user.organisation.all()[0]
    except IndexError:
        return HttpResponseForbidden()
    
    form = SearchForm(request.POST or None)
    if form.is_valid():
        buddies_in_range = []
        # geocode address
        lat, lng = geocode(request.POST.get('location'))
        # to keep things super simple, pull out all buddies, then filter in
        # memory. obviously this will have to be fixed once there is a
        # non-trivial number of buddies in the db. and when we have more 
        # than a day to work on this thing
        buddies = Buddy.objects.all()
        for buddy in buddies:
            buddy_lat, buddy_lng = float(buddy.location['latitude']), float(buddy.location['longitude'])
            radius = int(request.POST.get('radius'))
            dist = points2distance(((buddy_lng, 0, 0), (buddy_lat, 0, 0)),((lng, 0, 0), (lat, 0, 0)))
            if dist <= radius:
                buddies_in_range.append(buddy)
    else:
        buddies_in_range = None
        
    return render_to_response('buddies/search.html', {
        'form': form,
        'buddies_in_range': buddies_in_range
    }, context_instance=RequestContext(request))

def profile(request, pk=None):
    """
    Create or edit a buddy profile
    """
    if pk:
        # if editing, ensure that it is the correct user
        if not int(pk) == request.user.pk:
            return HttpResponseForbidden()
        instance = request.user.buddy.all()[0]
    else:
        try:
            Buddy.objects.get(user=request.user)
            return HttpResponseForbidden()
        except Buddy.DoesNotExist:
            pass
        instance = None
        
    form = ProfileForm(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        messages.success(request, 'Profile details have been updated')
        return redirect(reverse('buddies_detail', kwargs={'pk': obj.pk}))

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
            organisation = request.user.organisation.all()[0]
        except IndexError:
            return HttpResponseForbidden()
            
    try:
        organisation = request.user.organisation.all()[0]
    except IndexError:
        organisation = None
    if organisation:
        message_form = MessageForm(request.POST or None)
        if message_form.is_valid():
            contact = ContactLog(**{
                'service': organisation,
                'buddy': buddy,
                'message': message_form.cleaned_data['message']
            })
            contact.save()
            subject = 'You have a new message from refugeebuddy.org'
            message = render_to_string('buddies/email/buddy_message.txt', {'contact': contact})
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [buddy.email])
            messages.success(request, 'Your message has been sent')
            return redirect('.')

    return render_to_response('buddies/detail.html', {
        'buddy': buddy,
        'message_form': message_form
    }, context_instance=RequestContext(request))

@login_required
def message_response(request, action):
    """
    As a buddy, reply to a message sent by a refugee organisation
    """
    key = request.GET.get('key')
    contact = get_object_or_404(ContactLog, key=key)
    if not contact.buddy.user == request.user:
        return HttpResponseForbidden('You must be the buddy to whom this message was sent. If you are, please log in')
        
    if contact.response:
        pass # do something if there's already been a response
    
    contact.accepted = {'accept': True, 'reject': False}[action]
    contact.save()
    
    form = MessageResponseForm(request.POST or None)
    if form.is_valid():
        contact.response = form.cleaned_data['message']
        contact.save()
        subject = 'You have a response from refugeebuddy.org'
        message = render_to_string('buddies/email/buddy_message_response.txt', {'contact': contact})
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [contact.service.user.email])
        messages.success(request, 'Thanks for your response')
        return redirect('/')
        
    
    return render_to_response('buddies/message_response.html', {
        'form': form
    }, context_instance=RequestContext(request))
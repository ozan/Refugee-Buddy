from urllib import urlencode
from urllib2 import urlopen
try:
    import simplejson
except ImportError:
    from django.utils import simplejson
    
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

@login_required
def profile(request, pk=None):
    """
    Create or edit a buddy profile
    """
    if pk:
        # if editing, ensure that it is the correct user
        try:
            instance = request.user.buddy.get(pk=pk)
        except Buddy.DoesNotExist:
            return HttpResponseForbidden('You may not edit any profile other than your own.')
    else:
        try:
            request.user.buddy.all()[0]
            return HttpResponseForbidden('You may only create one profile.')
        except IndexError:
            pass
        instance = None
    
    if not instance and request.user.is_authenticated():
        name = request.user.username.replace('_', ' ')
        initial = {
            'name': name,
            'email': request.user.email,
            'preferred_name': name.partition(' ')[0]
        }
    else:
        initial = None
        
    form = ProfileForm(request.POST or None, instance=instance, initial=initial)
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
def my_detail(request):
    try:
        buddy = request.user.buddy.all()[0]
        return redirect(reverse('buddies_detail', kwargs={'pk': buddy.pk}))
    except IndexError:
        try:
            organisation = request.user.organisation.all()[0]
            return redirect(reverse('buddies_search'))
        except IndexError:
            return redirect(reverse('buddies_create'))
        

@login_required
def detail(request, pk):
    """
    View a buddy profile
    """
    buddy = get_object_or_404(Buddy, pk=pk)
    # if not viewing own profile, restrict to organisations
    try:
        request.user.buddy.get(pk=pk)
    except Buddy.DoesNotExist:
        try:
            organisation = request.user.organisation.all()[0]
        except IndexError:
            return HttpResponseForbidden()
            
    try:
        organisation = request.user.organisation.all()[0]
    except IndexError:
        organisation = None
    if organisation:
        message_form = MessageForm(request.POST or None, initial = {'message' : '''Dear <name>,

	Would you like to help out doing .......

	If you are able to help, you would need to be able to ....

	Please reply with your email address and phone number so that we can get in touch with you.

	Kind regards,

	<name>'''})
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
    else:
        message_form = None

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
    
    form = MessageResponseForm(request.POST or None, initial={'message' : '''Dear <name>,

Thankyou for your invitation to be part of your project.

I would/would be able to commit to participating. Please contact me on the following:

Phone: 
Email: 

Kind regards,

<name>'''})
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

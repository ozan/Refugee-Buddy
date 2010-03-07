from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

def home(request):
    if request.user.is_authenticated():
        return redirect('buddies_my_detail')
    return render_to_response('home.html', context_instance=RequestContext(request))

def faq(request):
    return render_to_response('faq.html', context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))


from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

def home(request):
    if request.user.is_authenticated():
        return redirect('buddies_my_detail')
    return render_to_response('static/home.html', context_instance=RequestContext(request))

def faq(request):
    return render_to_response('static/faq.html', context_instance=RequestContext(request))

def about(request):
    return render_to_response('static/about.html', context_instance=RequestContext(request))


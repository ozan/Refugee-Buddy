from django.contrib.auth import login, get_backends
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from forms import SignupForm

def signup(request):
    """
    Allow a new user to register an account.
    """
    form = SignupForm(request.POST or None)
    if form.is_valid():
        form.cleaned_data['username'] = form.cleaned_data['username'].replace(' ', '_')
        user = User.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
        backend = get_backends()[0]
        user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
        login(request, user)
        return redirect(reverse('buddies_create'))

    return render_to_response('accounts/signup.html',
                              {'form': form},
                              context_instance=RequestContext(request))

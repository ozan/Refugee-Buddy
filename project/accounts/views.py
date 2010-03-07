from django.conf import settings
from django.contrib.auth import login, get_backends
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

from forms import SignupForm

def signup(request):
    """
    Allow a new user to register an account.
    """
    form = SignupForm(request.POST or None)
    if form.is_valid():
        first_name = form.cleaned_data['username'].partition(' ')[0]
        form.cleaned_data['username'] = form.cleaned_data['username'].replace(' ', '_')
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        context_vars = {'username': username, 'email': email, 'password': password, 'first_name': first_name}
        user = User.objects.create_user(username=username, email=email, password=password)
        subject = render_to_string('accounts/email/register_subject.txt', context_vars).rstrip('\n')
        message = render_to_string('accounts/email/register_message.txt', context_vars)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        backend = get_backends()[0]
        user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
        login(request, user)
        return redirect(reverse('buddies_create'))

    return render_to_response('accounts/signup.html',
                              {'form': form},
                              context_instance=RequestContext(request))

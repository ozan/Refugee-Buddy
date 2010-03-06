from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.forms.widgets import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.template.loader import render_to_string

from contact.forms import ContactForm

def contact(request):
    form = ContactForm(request.POST or None)

    if form.is_valid():
        email_vars = {'name': form.cleaned_data['name'], 'email': form.cleaned_data['email'], 'subject': form.cleaned_data['subject'], 'message': form.cleaned_data['message']}
        subject = render_to_string('contact/email/contact_subject.txt', email_vars).rstrip('\n')
        message = render_to_string('contact/email/contact_message.txt', email_vars)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [form.cleaned_data['email']])
        return render_to_response('contact/thankyou.html', {},
            context_instance=RequestContext(request))
    else:
        return render_to_response('contact/form.html', {'form': form}, context_instance=RequestContext(request))

    return render_to_response('contact/form.html', {'form': form},
        context_instance=RequestContext(request))


from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^faq/$', direct_to_template, {'template': 'static/faq.html'}, name='faq'),
    url(r'^about/$', direct_to_template, {'template': 'static/about.html'}, name='about'),
)

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

static_urls = (
    'faq',
    'about',
    'messages',
    'resources',
    'terms',
    'disclaimer',
    'privacy',
    'copyright',
)

patterns_args = [url(r'^%s/$' % u, direct_to_template, {'template': 'static/%s.html' % u}, name=u) for u in static_urls]

urlpatterns = patterns('', *patterns_args)


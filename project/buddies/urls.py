from django.conf import settings
from django.conf.urls.defaults import *

from views import search, profile, detail

urlpatterns = patterns('',
    url(r'^search/$', search, name='buddies_search'),
    url(r'^profiles/create/', profile, name='buddies_create'),
    url(r'^profiles/(?P<pk>d+)/', detail, name='buddies_detail'),
    url(r'^profiles/(?P<pk>d+)/edit/', profile, name='buddies_edit'),
)
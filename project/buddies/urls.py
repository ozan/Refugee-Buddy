from django.conf import settings
from django.conf.urls.defaults import *

from views import search, profile, detail, message_response

urlpatterns = patterns('',
    url(r'^search/$', search, name='buddies_search'),
    url(r'^profiles/create/$', profile, name='buddies_create'),
    url(r'^profiles/(?P<pk>\d+)/$', detail, name='buddies_detail'),
    url(r'^profiles/(?P<pk>\d+)/edit/$', profile, name='buddies_edit'),
    
    url(r'^messages/accept/$', message_response, {'action': 'accept'}, name='buddies_response_accept'),
    url(r'^messages/reject/$', message_response, {'action': 'reject'}, name='buddies_response_reject'),
    
)

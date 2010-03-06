from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

from views import signup

urlpatterns = patterns('',

    url(r'^login/$', login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/$', signup, name='signup')
)

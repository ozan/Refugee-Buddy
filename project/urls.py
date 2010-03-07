from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template

from contact.views import contact
from library.views import home

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^contact/$', contact, name='contact'),
    (r'^static/', include('library.urls')),
    (r'^accounts/', include('accounts.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/media/img/favicon.ico'}),
    
    (r'^buddies/', include('buddies.urls')),
    
)

if settings.SERVE_MEDIA:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)	
EMAIL_FILE_PATH = getattr(settings, 'EMAIL_FILE_PATH', None)
if EMAIL_FILE_PATH:
    urlpatterns += patterns('',
        (r'^log/emails/(?P<path>.*)$', 'django.views.static.serve', 
            {'document_root': settings.EMAIL_FILE_PATH, 'show_indexes': True}),
    )


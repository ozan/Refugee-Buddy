from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template

from contact.views import contact

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'home.html'}, name='home'),
    url(r'^faq/$', direct_to_template, {'template': 'faq.html'}, name='faq'),
    url(r'^about/$', direct_to_template, {'template': 'about.html'}, name='about'),
    url(r'^contact/$', contact, name='contact'),
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


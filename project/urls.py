from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/media/img/favicon.ico'}),
    
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


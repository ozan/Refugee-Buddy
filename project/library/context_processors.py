from django.conf import settings

def setting_values(request):
    return {
        'SITE_DOMAIN': getattr(settings, 'SITE_DOMAIN', None),
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
    }
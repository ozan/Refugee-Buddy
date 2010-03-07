"""
http://squarefactor.com/words/2009/jan/06/django-custom-model-fields-with-custom-widget/
"""
from django.contrib.admin.widgets import AdminTextareaWidget
from django.db import models
try:
    import simplejson
except ImportError:
    from django.utils import simplejson
from django import forms
from django.conf import settings
from django.template.loader import render_to_string

from settings import geolocation_context as geosettings

class GeoLocationFieldWidget(AdminTextareaWidget):
    """ 
    The widget used to render the GeoLocationField 
    in the admin.
    Allows fine tuning of a geo-coded address with 
    a clickable google map.

    Assumes that the required js files are in the media js folder.
    * jquery.js
    * query.json-1.3.min.js
    * geo_location_field.js

    Also assumes that the google maps api key is 
    in the settings file under GOOGLE_MAPS_API_KEY.
    """

    def __init__(self, attrs=None):
        super(GeoLocationFieldWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        context = dict([(s, getattr(geosettings, s)) for s in dir(geosettings) if s == s.upper()])
        if type(value) == type(u''):
            try:
                value = simplejson.loads(value)
            except ValueError:
                value = {}
        context.update(locals())
        return render_to_string("geo_location_field.html", context)

    class Media:
    #try:
      js = ['http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js', 
            'js/geo_location_field.js', 
            'js/jquery.json-1.3.min.js',
            'http://maps.google.com/maps?file=api&v=2&key=' + settings.GOOGLE_MAPS_API_KEY,
            ]
    #except AttributeError:
    #  pass


class GeoLocationFormField(forms.fields.Field):
  """ 
  Used to validate the data submitted by
  the GeoLocationFieldWidget in the admin.
  """

  def clean(self, value):
    """ 
    Validates the json submitted and the required properties.
    """
    if super(GeoLocationFormField, self).clean(value):

      try:
        data = simplejson.JSONDecoder().decode(value)
      except ValueError:
        # This should never happen, but if by chance the front end builds bad json, we catch it here. The user has no options if this is happening, we will need to find the bug.
        raise forms.ValidationError('An error has occured. Unable to parse the geo encoded data for saving.')
        
      if self.required:
        # Now make sure the json has all of the required properties to save.
        if not data['address'] or len(data['address']) < 1:
          raise forms.ValidationError('Please provide a location or address.')

        if not data['latitude'] or len(data['latitude']) < 1 or not data['longitude'] or len(data['longitude']) < 1:
          raise forms.ValidationError('Please wait for the geo encoding of your location to complete before clicking save.')

    return value


class GeoLocationField(models.TextField):
  """ 
  Stores an address and the google geocoded 
  data for latitude and longitude.

  This data is automatically retrieved 
  from google when the location is saved.
  """

  __metaclass__ = models.SubfieldBase

  def to_python(self, value):

    if not value or isinstance(value, dict):
      return value

    try:
      value = simplejson.JSONDecoder().decode(value)
    except ValueError:
      value = {}

    return value

  def get_db_prep_value(self, value):
    return simplejson.JSONEncoder().encode(value)

  def formfield(self, **kwargs):

    kwargs['widget'] = GeoLocationFieldWidget
    kwargs['form_class'] = GeoLocationFormField

    return super(GeoLocationField, self).formfield(**kwargs)

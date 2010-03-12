from django import forms
from django.forms.widgets import *

from models import Buddy

RADIUS_CHOICES = (
    (1, '1km'),
    (10, '10km'),
    (100, '100km')
)

class ProfileForm(forms.ModelForm):
    name = forms.CharField(widget=HiddenInput())
    preferred_name = forms.CharField(max_length=80, label='You can call me')
    email = forms.CharField(widget=HiddenInput())

    class Meta:
        exclude = ('user',)
        model = Buddy
        
class SearchForm(forms.Form):
    location = forms.CharField(max_length=100, required=True)
    radius = forms.ChoiceField(choices=RADIUS_CHOICES)
    
    
class MessageFormBase(forms.Form):
    pass
    
class MessageForm(MessageFormBase):
    message = forms.CharField(widget=forms.Textarea(), required=True)
    
    
class MessageResponseForm(MessageFormBase):
    message = forms.CharField(widget=forms.Textarea(), required=True)
    
    
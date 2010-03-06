from django import forms

from models import Buddy

RADIUS_CHOICES = (
    (1, '1km'),
    (10, '10km'),
    (100, '100km')
)

class ProfileForm(forms.ModelForm):

    class Meta:
        exclude = ('user',)
        model = Buddy
        
class SearchForm(forms.Form):
    location = forms.CharField(max_length=100, required=True)
    radius = forms.ChoiceField(choices=RADIUS_CHOICES)

from django import forms

from models import Buddy

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Buddy
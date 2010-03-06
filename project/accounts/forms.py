from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import *

class SignupForm(UserCreationForm):
    """
    Signup form for Refugee Buddy.
    
    """
    
    username = forms.CharField(max_length=30,
        widget=forms.TextInput(),
        label="Full name")
    
    email = forms.EmailField(widget=forms.TextInput())
    
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError("Sorry, that email address is taken.")
        return self.cleaned_data['email']
    

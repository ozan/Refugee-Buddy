from django.contrib.auth.models import User
from django.db import models

from geolocation import GeoLocationField

from library.models import BaseModel


class ParticipationLevel(BaseModel):
    """
    An indication of a willingness to participate to a certain level
    """
    name = models.CharField(max_length=80)

    class Meta(BaseModel.Meta):
        pass

    def __unicode__(self):
        return self.name


class Buddy(BaseModel):
    """
    A volunteer on the Refugee Buddy service
    """
    name                = models.CharField(max_length=120, verbose_name='full name')
    preferred_name      = models.CharField(blank=True, max_length=80)
    age                 = models.CharField(blank=True, max_length=20, help_text='Please provide a general idea of your age range')
    email               = models.EmailField()
    phone               = models.CharField(max_length=14)
    
    location            = GeoLocationField()
    
    interests           = models.TextField()
    experience          = models.TextField(blank=True)
    
    participation_level = models.ManyToManyField(ParticipationLevel, related_name='buddies')
    
    user                = models.ForeignKey(User, related_name="buddy")

    class Meta(BaseModel.Meta):
        verbose_name_plural = 'buddies'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('buddies_detail', {'pk': self.pk})
        

class Organisation(BaseModel):
    """
    An refugee organisation registered with the Refugee Buddy service
    """
    user = models.ForeignKey(User, related_name="organisation")

    class Meta(BaseModel.Meta):
        pass

    def __unicode__(self):
        return NotImplementedError


class ContactLog(BaseModel):
    """
    An instance of contact being made by a service to a buddy
    """
    service     = models.ForeignKey(User, related_name="contacts")
    buddy       = models.ForeignKey(Buddy, related_name="contacts")
    message     = models.TextField()
    accepted    = models.BooleanField(default=True)
    response    = models.TextField(blank=True)

    class Meta(BaseModel.Meta):
        pass

    def __unicode__(self):
        raise NotImplementedError




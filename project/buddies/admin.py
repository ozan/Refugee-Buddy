from django.contrib import admin

from models import Buddy, ParticipationLevel, Organisation

admin.site.register((Buddy, ParticipationLevel, Organisation))
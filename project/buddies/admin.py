from django.contrib import admin

from models import Buddy, BuddyBlacklisting, ParticipationLevel, Organisation

admin.site.register((Buddy, BuddyBlacklisting, ParticipationLevel, Organisation))

from django.db import models

class VisibleManager(models.Manager):
    def visible(self):
        return self.filter(visible=True)
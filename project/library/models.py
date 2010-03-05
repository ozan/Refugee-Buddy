from datetime import datetime

from django.db import models

class BaseModel(models.Model):
    """
    Base model for all model objects in the project.
    
    Subclass this, unless you're sure that we don't need to store the
    metadata that this model defines.
    """
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

        
class BaseContent(BaseModel):
    visible         = models.BooleanField(blank=True, verbose_name='Visible on site')
    published       = models.DateTimeField(null=True)
    
    class Meta(BaseModel.Meta):
        abstract = True
        
    def save(self, force_insert=False, force_update=False):
        if self.visible and not self.published:
            self.published = datetime.now()
        if self.published and not self.visible:
            self.published = None    
        super(BaseModel, self).save(force_insert, force_update)

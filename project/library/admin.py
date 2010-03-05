from copy import deepcopy

from django.contrib import admin

from django.contrib.admin.util import flatten_fieldsets


class BaseFieldPermAdmin(admin.ModelAdmin):
    """ModelAdmin wrapper for restricting fields based on the request/obj"""

    def get_restricted_fields(self, request, obj=None):
        """Hook to specify restricted fields, override this"""
        return []
        
    def get_fieldsets(self, request, obj=None):
        fieldsets = deepcopy(super(BaseFieldPermAdmin, self).get_fieldsets(request, obj))
        restricted_fields = self.get_restricted_fields(request, obj)
        for fs in fieldsets:
            fs[1]['fields'] = [ f for f in fs[1]['fields'] if f not in restricted_fields ]
        return fieldsets

    def get_form(self, request, obj=None, fields=None, **kwargs):
        fields = flatten_fieldsets(self.get_fieldsets(request, obj))
        return super(BaseFieldPermAdmin, self).get_form(request, obj, fields=fields, **kwargs)
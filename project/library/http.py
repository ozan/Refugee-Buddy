from django.core.serializers import json, serialize
from django.db.models.query import QuerySet
from django.http import HttpResponse

try:
    import simplejson
except ImportError:
    from django.utils import simplejson


class JsonResponse(HttpResponse):
    def __init__(self, obj):
        if isinstance(obj, QuerySet):
            content = serialize('json', obj)
        else:
            content = simplejson.dumps(obj, indent=2, 
                cls=json.DjangoJSONEncoder, ensure_ascii=False)
        super(JsonResponse, self).__init__(content, 
            content_type='application/json')

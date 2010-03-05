import unicodedata
import re
from htmlentitydefs import name2codepoint

from django.utils.encoding import force_unicode

# Snippet taken from http://www.djangosnippets.org/snippets/1030/

def slugify(s, entities=False, decimal=False, hexadecimal=False, invalid=None,
        instance=None, manager=None, slug_field='slug', extra_lookup=None):
    """
    Will try to make the best url string out of any string. If the `entities`
    keyword is True it will try to translate html entities. The `decimal`
    keyword is for decimal html character reference, `hexadecimal` for
    hexadecimal.
    `invalid` should be a list or tuple of invalid slugs. You can also pass
    a Django model instance as `instance`, slugify will then make sure it is a
    unique slug for that model. The keyword `extra_lookup` should be a
    dictionary containing extra lookup. Use this to make the slug unique only
    within the the lookup. For example:
    extra_lookup = {'date': datetime.date.today()} slugify will make
    the slug unique for rows where the column 'date' is todays date. `slug_field`
    is the field in the model to match for uniqueness. You can pass a manager
    to use instead of the default one as `manager`.
    """
    s = force_unicode(s)
    if entities:
        s = re.sub('&(%s);' % '|'.join(name2codepoint),
                lambda m: unichr(name2codepoint[m.group(1)]), s)
    if decimal:
        try:
            s = re.sub('&#(\d+);',
                    lambda m: unichr(int(m.group(1))), s)
        except ValueError:
            pass
    if hexadecimal:
        try:
            s = re.sub('&#x([\da-fA-F]+);',
                    lambda m: unichr(int(m.group(1), 16)), s)
        except ValueError:
            pass
    
    #translate
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
    #replace unwanted characters
    s = re.sub(r'[^-a-z0-9]+', '-', s.lower())
    #remove redundant -
    s = re.sub('-{2,}', '-', s).strip('-')

    invalid = invalid or []
    if instance:
        lookup = extra_lookup or {}
        if not manager:
            manager = instance.__class__._default_manager
    
    slug, counter = s, 2
    while True:
        if slug in invalid:
            pass
        elif not instance:
            return slug
        else:
            lookup[slug_field] = slug
            qs = manager.filter(**lookup)
            if instance.pk:
                qs = qs.exclude(pk=instance.pk)
            if not qs.count():
                return slug
        slug = "%s-%s" % (s, counter)
        counter += 1
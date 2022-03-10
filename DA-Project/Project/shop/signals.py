from django.utils.text import slugify
import random
from unidecode import unidecode

def create_slug(instance, new_slug=None):  
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(unidecode(instance.name))
    
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        rd = round(random.random()*100000)
        new_slug = slug + f'-{rd}'

        return create_slug(instance, new_slug=new_slug)
    return slug
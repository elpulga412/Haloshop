from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from ckeditor.fields import RichTextField
from django.utils.text import slugify
import random
from unidecode import unidecode
from django.conf import settings
import datetime

# Create your models here.


User = settings.AUTH_USER_MODEL

def upload_home(instance, filename):
    date = datetime.datetime.now()
    print(filename)
    return f'News/IMG_news_upload_{date.strftime("%d")}-{date.strftime("%m")}-{date.strftime("%y")}/{filename}'

class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=120, blank=True, null=True)
    image = models.ImageField(upload_to=upload_home, blank=True, null=True)
    content = RichTextField(blank=True, null=True)
    slug = models.SlugField(max_length=120, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

def create_slug(instance, new_slug=None):  
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(unidecode(instance.title))
    
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        rd = round(random.random()*100000)
        new_slug = slug + f'-{rd}'

        return create_slug(instance, new_slug=new_slug)
    return slug


@receiver(pre_save, sender=News)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
       instance.slug = create_slug(instance)
    
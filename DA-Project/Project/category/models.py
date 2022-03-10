from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from shop.signals import create_slug
from shop.links import category_link
from ckeditor.fields import RichTextField
# Create your models here.

def upload_location(instance, filename):
    folder_name = (instance.__class__.__name__).lower()
    return f'{folder_name}/{filename}'

class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Thương hiệu")
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    description = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def urlImage(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def get_category_link(self):
        return category_link(self)


@receiver(pre_save, sender=Category)
def pre_save_receiver(sender, instance, *args, **kwargs):
    instance.name = instance.name.upper()
    if not instance.slug:
       instance.slug = create_slug(instance)

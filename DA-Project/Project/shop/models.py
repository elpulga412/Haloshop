from django.db import models
from django.db.models.base import Model
from django.dispatch import receiver
from django.db.models.signals import pre_save
from shop.signals import create_slug
from category.models import Category
from .links import series_link, product_link
import datetime
from ckeditor.fields import RichTextField
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL

def upload_home(instance, filename):
    date = datetime.datetime.now()
    print(filename)
    return f'IMG_home_upload_{date.strftime("%d")}-{date.strftime("%m")}-{date.strftime("%y")}/{filename}'


def upload_location(instance, filename):
    date = datetime.datetime.now()
    print(filename)
    return f'IMG_detail_upload_{date.strftime("%d")}-{date.strftime("%m")}-{date.strftime("%y")}/{filename}'


class Series(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100, null=True, verbose_name="Version")
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super(Series, self).save(*args, **kwargs)

    def get_series_link(self):
        return series_link(self)


@receiver(pre_save, sender=Series)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
       instance.slug = create_slug(instance)

class Version(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100, null=True, verbose_name="Version Name")
    image = models.ImageField(upload_to=upload_home, blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)
    
    def get_rating(self):
        ratings = self.reviewrating_set.all()
        count = ratings.count()
        total = 0
        for index in ratings:
            total += int(index.rating)
        try:
            average = total / count
        except ZeroDivisionError:
            average = 0
        return average

    def get_vote(self):
        ratings = self.reviewrating_set.all().count()
        return ratings

CAPACITY = [
    ('32GB', '32GB'),
    ('64GB', '64GB'),
    ('128GB', '128GB'),
    ('256GB', '256GB'),
    ('512GB', '512GB'),
    ('1TB', '1TB'),
] 


class Product(models.Model): 
    version = models.ForeignKey(Version, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Tên sản phẩm', related_name='product')  
    slug = models.SlugField(max_length=200, blank=True, unique=True)
    capacity = models.CharField(max_length=10, choices=CAPACITY, default='128GB')
    price = models.IntegerField(blank=True, null=True, verbose_name='Giá')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.version)  + " " + self.capacity

    def imageURL(self):
        try:
            url = self.version.image.url
        except:
            url = ""
        return url

    def get_product_url(self):
        return product_link(self)

@receiver(pre_save, sender=Product)
def pre_save_receiver(sender, instance, *args, **kwargs):
    instance.name = instance.version.name.title() + '-' + instance.capacity
    if not instance.slug:
       instance.slug = create_slug(instance)



class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Sản phẩm')
    color = models.CharField(max_length=20, blank=True, null=True, verbose_name='Màu')
    image = models.ImageField(upload_to=upload_location, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True, verbose_name='Số lượng')
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.product)

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class ReviewRating(models.Model):
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True, null=True)
    review = models.TextField(max_length=500, blank=True, null=True)
    rating = models.FloatField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
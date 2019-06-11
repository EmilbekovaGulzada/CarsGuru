from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from tinymce.models import HTMLField
from django.db.models.signals import pre_save

# from gigant.utils import unique_slug_generator


class Category(models.Model):
    title = models.CharField(max_length=255)  # High technology
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title


def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(category_pre_save_receiver, sender=Category)

def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(str(instance.name), reversed=True))
        instance.slug = slug

        pre_save.connect(pre_save_category_slug, sender=Category)


class Product(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to="CarsGuru/image_folder/product_images")
    price = models.PositiveIntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'pk': self.pk})



def image_folder(instance, filename):
    filename = instance.slug = '.' + filename.split('.')[1]
    return "{0}/{1}".format(instance.slug, filename)


class CarManager(models.Manager):

    def all(self, *args, **kwargs):
        return super(CarManager, self).get_queryset().filter(available=True)


class Car(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to="CarsGuru/image_folder/product_image")
    available = models.BooleanField(default=True)

    objects = CarManager()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from transliterate import translit



# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)


    def __str__(self):
        return self.name



def pre_save_category_slug(sender, instance, *args, **kwargs):
    if  not instance.slug:
        slug = slugify(translit(str(instance.name), reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_category_slug, sender=Category)


class Mark(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


def image_folder(instance, filename):
    filename = instance.slug ='.' + filename.split('.')[1]
    return "{0}/{1}".format(instance.slug, filename)

class ProductManager(models.Manager):

    def all(self, *args, **kwargs):
        return super(ProductManager, self).get_queryset().filter(available=True)



class Product(models.Model):

    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to=image_folder)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    available = models.BooleanField(default=True)
    object = ProductManager

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return


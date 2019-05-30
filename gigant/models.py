from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from tinymce.models import HTMLField
from django.db.models.signals import pre_save

from gigant.utils import unique_slug_generator






# from django.core.urlresolvers import reverse
# from transliterate import translit


# class Category(models.Model):
#     name = models.CharField(max_length=200)
#     slug = models.SlugField()
#     parent = models.ForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
#
#     class Meta:
#         unique_together = ('slug', 'parent',)    #enforcing that there can not be two
#         verbose_name_plural = "categories"       #categories under a parent with same
#                                                  #slug
#
#     def get_absolute_url(self):
#         return reverse('product', kwargs={'slug': self.slug})
#
#     def __str__(self):                           # __str__ method elaborated later in
#         full_path = [self.name]                  # post.  use __unicode__ in place of
#                                                  # __str__ if you are using python 2
#         k = self.parent
#
#         while k is not None:
#             full_path.append(k.name)
#             k = k.parent
#
#         return ' -> ' .join(full_path[::-1])






class Category(models.Model):
    title = models.CharField(max_length=255)  # High technology
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})


def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)





pre_save.connect(category_pre_save_receiver, sender=Category)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)
    content = HTMLField('Content', null=True)
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False, )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def get_cat_list(self):  # for now ignore this instance method,
        k = self.category
        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent

        for i in range(len(breadcrumb) - 1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i - 1:-1])
        return breadcrumb[-1:0:-1]


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
    price = models.DecimalField(max_digits=9, decimal_places=2)
    available = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):


        return reverse('product_detail', kwargs={'product_slug': self.slug})

name = models.CharField(max_length=100)


def __str__(self):
    return self.name


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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


# @receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


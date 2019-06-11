from django.contrib import admin
from gigant.models import Category,Product, Car


# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['id', '__str__', 'parent']


admin.site.register(Category)
admin.site.register(Car)
admin.site.register(Product)


# Register your models here.



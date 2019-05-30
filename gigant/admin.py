from django.contrib import admin
from gigant.models import Category,Product, Car


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__', 'parent']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Car)
admin.site.register(Product)

# admin.site.register(CartItem)
# admin.site.register(Cart)
# Register your models here.



from django.shortcuts import render

# Create your views here.
from gigant.models import Category, Product




def base_view(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'base.html', {})





def product_view(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    context = {
        'product': product

    }
    return  render(request, 'product.html', context)


def category_view(request, category_slug):
    Category = Category.objects.get(slug=category_slug)
    context = {
        'category': category

    }
    return render(request, 'category.html', context)

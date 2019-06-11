from datetime import date

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_text
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.generic import DetailView, ListView
from django.conf import settings
# Create your views here.
from gigant.models import Category, Car,  Product


# from gigant.tokens import account_activation_token
from gigant.forms import SignUpForm, OrderForm


def base_view(request):
    categories = Category.objects.all()
    car = Car.objects.all()

    return render(request, 'base.html', context={
        'categories': categories,
        'cars': car,

    })


def about_page(request):
    context = {
        "title": "About page",
                 "content": " Welcome to the about page."
    }
    return render(request, "about.html", context)


def contacts_page(request):
    context = {
        "title": "About page",
                 "content": " Welcome to the about page."
    }
    return render(request, "contacts.html", context)




def car_view(request, car_slug):
    car = Car.objects.get(slug=car_slug)
    categories = Category.objects.all()
    context = {
        'car': car,
        'categories': categories

    }
    return render(request, 'car.html', context)


def category_view(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    cars_of_category = Car.objects.filter(category=category)
    context = {
        'category': category,
        'cars_of_category': cars_of_category

    }
    return render(request, 'category.html', context)


def product_view(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            send_mail(
                subject='Order from site',
                message='''
                    new order from {date} 
                    name: {name}
                    email: {email}
                    phone: {phone}
                    
                    with message:
                    ------------------------
                    {message}
                    ------------------------
                '''.format(
                    date=date.today(),
                    name=form.cleaned_data.get('name'),
                    email=form.cleaned_data.get('email'),
                    phone=form.cleaned_data.get('phone'),
                    message=form.cleaned_data.get('message'),
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['emilbekovagulzada.kg@gmail.com', 'dan.tyan@gmail.com']
            )
            return redirect(request.build_absolute_uri())
        else:
            print(form.errors)
    else:
        form = OrderForm()
    context = {
        'product': product,
        'form': form
    }
    return render(request, 'product.html', context)


def show_category(request, car_slug, category_slug):
    category_slug = hierarchy.split('/')
    category_queryset = list(Category.objects.all())
    all_slugs = [x.slug for x in category_queryset]
    parent = None
    for slug in category_slug:
        if slug in all_slugs:
            parent = get_object_or_404(Category, slug=slug, parent=parent)
        else:
            instance = get_object_or_404(Post, slug=slug)
            breadcrumbs_link = instance.get_cat_list()
            category_name = [' '.join(i.split('/')[-1].split('-')) for i in breadcrumbs_link]
            breadcrumbs = zip(breadcrumbs_link, category_name)
            return render(request, "postDetail.html", {'instance': instance, 'breadcrumbs': breadcrumbs})

    return render(request, "category.html",
                  {'post_set': parent.post_set.all(), 'sub_categories': parent.children.all()})


class CategoryView(ListView):
    template_name = 'product_list.html'
    model = Product
    category = None

    def dispatch(self, request, *args, **kwargs):
        self.car = get_object_or_404(Car, slug=kwargs.get('slug'))

        if kwargs.get('category_slug'):
            self.category = get_object_or_404(Category, slug=kwargs.get('category_slug'))

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(car=self.car)
        if self.category:
            queryset = queryset.filter(category=self.category)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['car'] = self.car
        context['current_category'] = self.category
        context['categories'] = Category.objects.filter(parent__isnull=True).prefetch_related('children')
        return context




from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_text
from django.contrib.auth import login
from django.contrib.auth.models import User

# Create your views here.
from gigant.models import Category, Car, Post

# from gigant.tokens import account_activation_token
from gigant.forms import SignUpForm

def base_view(request):
    categories = Category.objects.all()
    car = Car.objects.all()

    return render(request, 'base.html', context = {
        'categories': categories,
        'cars': car,
    })





def car_view(request, car_slug):
    car = Car.objects.get(slug=car_slug)
    categories = Category.objects.all()
    context = {
        'cars': car,
        'categories': categories

    }
    return  render(request, 'car.html', context)


def category_view(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    cars_of_category = Car.objects.filter(category=category)
    context = {
        'category': category,
        'cars_of_category': cars_of_category

    }
    return render(request, 'category.html', context)

# def cart_view(request):
#     cart = Cart.objects.first()
#     context = {
#         'cart':cart
#     }
#     return render(request, 'cart.html', context)


def show_category(request, car_slug, category_slug):

    category_slug = hierarchy.split('/')
    category_queryset = list(Category.objects.all())
    all_slugs = [ x.slug for x in category_queryset ]
    parent = None
    for slug in category_slug:
        if slug in all_slugs:
            parent = get_object_or_404(Category,slug=slug,parent=parent)
        else:
            instance = get_object_or_404(Post, slug=slug)
            breadcrumbs_link = instance.get_cat_list()
            category_name = [' '.join(i.split('/')[-1].split('-')) for i in breadcrumbs_link]
            breadcrumbs = zip(breadcrumbs_link, category_name)
            return render(request, "postDetail.html", {'instance':instance,'breadcrumbs':breadcrumbs})

    return render(request,"categories.html",{'post_set':parent.post_set.all(),'sub_categories':parent.children.all()})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')
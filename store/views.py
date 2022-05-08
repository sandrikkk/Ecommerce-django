from django.shortcuts import get_object_or_404, render
from store.models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.

def store(request, category_slug = None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category , slug = category_slug)
        products = Product.objects.filter(category = categories, is_available = True)
        paginator = Paginator(products,1)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available = True).order_by('id')
        paginator = Paginator(products,3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_product,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug = category_slug, slug = product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product = single_product).exists()

    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET: # ამოწმებს Search ში არის თუ არა keyword
        keyword = request.GET['keyword'] 
        if keyword: #ამოწმებს keyword ცარიელია თუ არა...
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains = keyword) | Q(product_name__icontains = keyword))
            #filter(description__icontains = keyword) თუ ამ პროდუქციის აღწერა შეიცავს Keyword -ს 
            #Q = Quary_set
            product_count = products.count() # ითვლის თუ რამდენი ობიექტი მოიძებნა ..

        context = {
            'products': products,
            'product_count': product_count
        }

    return render(request, 'store/store.html', context)
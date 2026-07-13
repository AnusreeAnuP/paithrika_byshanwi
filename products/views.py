from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category

def home(request):
    new_arrivals = Product.objects.filter(is_available=True, is_new_arrival=True)[:8]
    best_sellers = Product.objects.filter(is_available=True, is_best_seller=True)[:4]
    paithrika_categories = Category.objects.filter(brand='paithrika')
    context = {
        'new_arrivals': new_arrivals,
        'best_sellers': best_sellers,
        'paithrika_categories': paithrika_categories,
    }
    return render(request, 'home.html', context)

def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, is_available=True)
    return render(request, 'products/category_detail.html', {'category': category, 'products': products})

def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_available=True)
    related_products = Product.objects.filter(category=product.category, is_available=True).exclude(id=product.id)[:4]
    return render(request, 'products/product_detail.html', {'product': product, 'related_products': related_products})

def search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query),
            is_available=True
        ).distinct()
    return render(request, 'products/search_results.html', {'results': results, 'query': query})

def about_us(request):
    return render(request, 'pages/about_us.html')

def contact_us(request):
    submitted = False
    if request.method == 'POST':
        submitted = True
    return render(request, 'pages/contact_us.html', {'submitted': submitted})
# ... Keep your existing views exactly as they are, then add these at the end:

def privacy_policy(request):
    return render(request, 'pages/privacy_policy.html')

def terms_conditions(request):
    return render(request, 'pages/terms_conditions.html')

def dremora_home(request):
    """Landing page for Dremora stitching unit."""
    dremora_categories = Category.objects.filter(brand='dremora')
    # Collect up to 4 featured products across all Dremora categories
    featured_products = Product.objects.filter(
        category__brand='dremora', is_available=True
    ).order_by('-created_at')[:8]
    context = {
        'dremora_categories': dremora_categories,
        'featured_products': featured_products,
    }
    return render(request, 'dremora/home.html', context)
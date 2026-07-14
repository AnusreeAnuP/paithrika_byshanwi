from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Wishlist, WishlistItem
from products.models import Product

def _get_or_create_wishlist(request):
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        wishlist, created = Wishlist.objects.get_or_create(session_key=session_key)
    return wishlist

def wishlist_detail(request):
    wishlist = _get_or_create_wishlist(request)
    items = wishlist.items.select_related('product')
    return render(request, 'wishlist/wishlist_detail.html', {'wishlist': wishlist, 'items': items})

def wishlist_add(request, product_id):
    wishlist = _get_or_create_wishlist(request)
    product = get_object_or_404(Product, id=product_id)
    
    wishlist_item, created = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
    if created:
        messages.success(request, f'Added {product.name} to your wishlist.')
    else:
        messages.info(request, f'{product.name} is already in your wishlist.')
    
    return redirect(request.META.get('HTTP_REFERER', 'wishlist:wishlist_detail'))

def wishlist_remove(request, wishlist_item_id):
    wishlist = _get_or_create_wishlist(request)
    wishlist_item = get_object_or_404(WishlistItem, id=wishlist_item_id, wishlist=wishlist)
    wishlist_item.delete()
    messages.success(request, 'Item removed from your wishlist.')
    return redirect(request.META.get('HTTP_REFERER', 'wishlist:wishlist_detail'))

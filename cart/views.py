from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product

def _get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def cart_detail(request):
    cart = _get_or_create_cart(request)
    items = cart.items.select_related('product')
    total = sum(item.get_total_price() for item in items)
    
    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'items': items,
        'total': total
    })

def cart_add(request, product_id):
    cart = _get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    messages.success(request, f'Added {product.name} to your cart.')
    return redirect('cart:cart_detail')

def cart_remove(request, cart_item_id):
    cart = _get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)
    cart_item.delete()
    messages.success(request, 'Item removed from your cart.')
    return redirect('cart:cart_detail')

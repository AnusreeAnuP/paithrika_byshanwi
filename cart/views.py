import urllib.parse
from django.conf import settings
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
    
    # Build WhatsApp Order Message
    whatsapp_number = getattr(settings, 'WHATSAPP_NUMBER', '918086297803')
    whatsapp_text = "Hi Paithrika, I would like to place an order for the following items:\n\n"
    for item in items:
        whatsapp_text += f"- *{item.product.name}* x {item.quantity} = ₹{item.get_total_price()}\n"
    whatsapp_text += f"\nTotal Amount: *₹{total}*"
    
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={urllib.parse.quote(whatsapp_text)}"
    
    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'items': items,
        'total': total,
        'whatsapp_url': whatsapp_url
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

def cart_update_quantity(request, cart_item_id, action):
    cart = _get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)
    
    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from your cart.')
            
    return redirect('cart:cart_detail')

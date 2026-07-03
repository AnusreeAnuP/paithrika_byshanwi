from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart, CartItem
from .models import Order, OrderItem

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')
        
    items = cart.items.all()
    total = sum(item.get_total_price() for item in items)
    
    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            postal_code=request.POST.get('postal_code')
        )
        
        # Create order items
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
            
        # Clear cart
        cart.items.all().delete()
        messages.success(request, 'Your order has been placed successfully!')
        return redirect('orders:order_history')
        
    return render(request, 'orders/checkout.html', {
        'items': items,
        'total': total
    })

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

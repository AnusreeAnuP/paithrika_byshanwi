from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncMonth
from orders.models import Order, OrderItem
from products.models import Product, Category
from accounts.models import CustomUser
from django.utils import timezone
from datetime import timedelta

@staff_member_required
def dashboard_home(request):
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(
        rev=Sum(F('items__price') * F('items__quantity'))
    )['rev'] or 0
    total_products = Product.objects.count()
    total_customers = CustomUser.objects.filter(is_staff=False).count()

    recent_orders = Order.objects.order_by('-created_at')[:5]
    low_stock = Product.objects.filter(stock__lt=10, is_available=True).order_by('stock')[:5]

    # Orders by status
    order_status = Order.objects.values('status').annotate(count=Count('id'))

    # Monthly revenue for last 6 months
    six_months_ago = timezone.now() - timedelta(days=180)
    monthly_revenue = (
        Order.objects
        .filter(created_at__gte=six_months_ago)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum(F('items__price') * F('items__quantity')))
        .order_by('month')
    )

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'total_customers': total_customers,
        'recent_orders': recent_orders,
        'low_stock': low_stock,
        'order_status': order_status,
        'monthly_revenue': monthly_revenue,
    }
    return render(request, 'dashboard/home.html', context)

@staff_member_required
def sales_report(request):
    orders = Order.objects.order_by('-created_at')
    total_revenue = orders.aggregate(
        rev=Sum(F('items__price') * F('items__quantity'))
    )['rev'] or 0
    top_products = (
        OrderItem.objects
        .values('product__name', 'product__category__name')
        .annotate(
            units_sold=Sum('quantity'),
            revenue=Sum(F('price') * F('quantity'))
        )
        .order_by('-units_sold')[:10]
    )
    context = {
        'orders': orders,
        'total_revenue': total_revenue,
        'top_products': top_products,
    }
    return render(request, 'dashboard/sales_report.html', context)

from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_available', 'is_new_arrival', 'is_best_seller', 'has_offer')
    list_filter = ('category', 'is_available', 'is_new_arrival', 'is_best_seller', 'has_offer')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

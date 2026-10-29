from django.contrib import admin
from .models import Product,Order,OrderItem,Wishlist,Review
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin): list_display=('name','category','price','stock','created_at');search_fields=('name','description')
class ItemInline(admin.TabularInline): model=OrderItem;extra=0
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin): list_display=('id','user','full_name','total_amount','status','created_at');inlines=[ItemInline]

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin): list_display=('user','product','created_at'); list_filter=('created_at',); search_fields=('user__username','product__name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin): list_display=('product','user','rating','created_at'); list_filter=('rating','created_at'); search_fields=('product__name','user__username','comment')

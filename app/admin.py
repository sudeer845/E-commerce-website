from django.contrib import admin
from .models import Product, Customer,Cart, Payment, OrderPlaced, Wishlist

# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','discount_price','category','product_img']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','locality','city','state','pincode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display=['id','user','amount','razorpay_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','ordered_date','status','payment']

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product']
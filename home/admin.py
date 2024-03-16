from django.contrib import admin
from .models import Fooditem,Cart,CartItem,Category,Rating
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','description']


@admin.register(Fooditem)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['id','Name','quantity','price','active','image']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','created_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id','cart','food_item','quantity']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id','food_item','score','review','created_at','user']

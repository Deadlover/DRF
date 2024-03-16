from .models import *
from rest_framework import serializers
from django.shortcuts import get_object_or_404

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields='__all__'

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model= Fooditem
        fields='__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model= Rating
        fields='__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Cart
        fields='__all__'

class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    food_item = FoodSerializer()
    class Meta:
        model  = CartItem
        fields='__all__'

    

class AddCartItemSerializer(serializers.ModelSerializer):
    food_item_id = serializers.IntegerField()
    
    def validate_food_item_id(self, value):
        if not Fooditem.objects.filter(pk=value).exists():
            raise serializers.ValidationError("There is no product associated with the given ID")
        
        return value
    
    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["food_item_id"] 
        print(product_id)
        quantity = self.validated_data["quantity"] 

        
        try:
            print('kkk')
            cartitem = CartItem.objects.get(cart=cart_id, food_item=product_id)
            cartitem.quantity += quantity
            cartitem.save()
            
            self.instance = cartitem
            
        
        except:
            
            self.instance = CartItem.objects.create(cart=cart_id, **self.validated_data)
            
        return self.instance
         

    class Meta:
        model = CartItem
        fields = [ "food_item_id", "quantity"]

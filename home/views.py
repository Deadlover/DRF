from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from .serializer import *
from rest_framework import status

 
class CategoryApi(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        category = Category.objects.all()
        serializer = CategorySerializer(category,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'data created'},status=status.HTTP_201_CREATED)
    
    def post(self,request):
        pk= request.data.get('pk')
        try:
            category  = Category.objects.get(id=pk)
            serializer = CategorySerializer(category,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'partial data updated'})
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"msg":"failed"},status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request):
        pk= request.data.get('pk')
        try:
            category  = Category.objects.get(id=pk)
            serializer = CategorySerializer(category,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'partial data updated'})
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"msg":"failed"},status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self,request):
        pk= request.data.get('pk')
        try:
            category  = Category.objects.get(id=pk)
            category.delete()
            return Response({'msg':' data deleted'})
        except:
            return Response({"msg":"failed"},status=status.HTTP_400_BAD_REQUEST)
    
    
class UploadApi(APIView):
    permission_classes=[IsAdminUser]
            
    def post(self,request):
        serializer = FoodSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'data created'},status=status.HTTP_201_CREATED)
    
    def put(self,request):
        pk= request.data.get('pk')
        try:
            fooditem  = Fooditem.objects.get(id=pk)
            serializer = FoodSerializer(fooditem,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'data updated'},status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
           return Response({"msg":"failed"},status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request):
        pk= request.data.get('pk')
        try:
            fooditem  = Fooditem.objects.get(id=pk)
            serializer = FoodSerializer(fooditem,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'partial data updated'})
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"msg":"failed"},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        pk= request.data.get('pk')
        try:
            fooditem  = Fooditem.objects.get(id=pk)
            fooditem.delete()
            return Response({'msg':' data deleted'})
        except:
            return Response({"msg":"failed"},status=status.HTTP_400_BAD_REQUEST)   

class RatingApi(APIView):
    pass


class MenuApi(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,format=None):
        food = Fooditem.objects.all()
        serializer = FoodSerializer(food,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class Add_To_CartApi(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self, request):
        user = request.user
        print(user)
        cart, created = Cart.objects.get_or_create(user=user)
        queryset = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(queryset,many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        # Assuming the Cart model has a relation to the User model
        cart, created = Cart.objects.get_or_create(user=user)
        
        # Passing the cart_id to the serializer context
        serializer = AddCartItemSerializer(
            data=request.data, 
            context={'cart_id': cart}
            )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        
        cart_item_id = request.data.get('cart_item_id')
        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
        except CartItem.DoesNotExist:
            return Response({'error': "CartItem not found"}, status=404)
        
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': "Item updated successfully"})
        else:
            return Response(serializer.errors, status=400)
    

    def delete(self, request):
        user = request.user
        data = request.data
        item_id = data.get('cart_item_id')

        if not item_id:
            return Response({'error': 'Missing food item id'}, status=400)
        
        cart = Cart.objects.filter(user=user).first()
        if not cart:
            return Response({'error': 'Cart not found'}, status=404)

        cart_items = CartItem.objects.filter(cart=cart, id=item_id)
        
        if not cart_items.exists():
            return Response({'error': 'CartItem not found in the cart'}, status=404)

        cart_items.delete()

        updated_cart_items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(updated_cart_items, many=True)
        return Response(serializer.data)




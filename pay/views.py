from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import *
from home.serializer import *
from rest_framework import status


class CreateOrderAPI(APIView):
    permission_classes = []  # Update this based on your requirements

    def get(self, request):
        user = request.user
        order, created = Order.objects.get_or_create(user=user)
        queryset = OrderItem.objects.filter(order=order)
        serializer = CartItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user

        try:
            cart = Cart.objects.get(
                user=user, is_active=True
            )  # Assuming an `is_active` field to find the active cart
        except Cart.DoesNotExist:
            return Response(
                {"error": "Active cart not found."}, status=status.HTTP_404_NOT_FOUND
            )

            # Create a new order
        order = Order.objects.create(
            user=user,
            is_complete=False,
            is_paid=False,
            total_price=0,
        )

        # Transfer cart items to order items
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = 0
        for item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                food_item=item.food_item,
                quantity=item.quantity,
                price=item.food_item.price * item.quantity,
            )
            total_price += order_item.price

        order.total_price = total_price
        order.save()

        cart_items.delete()

        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

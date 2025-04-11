from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from store.models import Cart, CartItem, Product
from store.serializers.cart_serializers import CartSerializer


class CartDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)

        if product.stock < quantity:
            return Response({'error': 'Not enough stock available'}, status=400)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return Response({'message': 'Item added to cart'}, status=200)


class RemoveFromCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')

        try:
            cart = Cart.objects.get(user=request.user)
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.delete()
            return Response({'message': 'Item removed from cart'}, status=200)
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response({'error': 'Item not found in cart'}, status=404)


class UpdateCartItemQuantityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if quantity < 1:
            return Response({'error': 'Quantity must be at least 1'}, status=400)

        try:
            cart = Cart.objects.get(user=request.user)
            item = CartItem.objects.get(cart=cart, product_id=product_id)

            if item.product.stock < quantity:
                return Response({'error': 'Not enough stock available'}, status=400)

            item.quantity = quantity
            item.save()
            return Response({'message': 'Quantity updated successfully'}, status=200)
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response({'error': 'Item not found in cart'}, status=404)

from rest_framework import generics
from store.models import Cart
from store.serializers.cart_serializers import CartSerializer

class CartListCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

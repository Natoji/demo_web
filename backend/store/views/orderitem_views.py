from rest_framework import generics
from store.models import OrderItem
from store.serializers.orderitem_serializers import OrderItemSerializer

class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class OrderItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

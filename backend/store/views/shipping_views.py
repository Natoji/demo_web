from rest_framework import generics
from store.models import ShippingInfo
from store.serializers.shippinginfo_serializers import ShippingInfoSerializer

class ShippingInfoListCreateView(generics.ListCreateAPIView):
    queryset = ShippingInfo.objects.all()
    serializer_class = ShippingInfoSerializer

class ShippingInfoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShippingInfo.objects.all()
    serializer_class = ShippingInfoSerializer

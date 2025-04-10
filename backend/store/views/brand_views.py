from rest_framework import generics
from store.models import Brand
from store.serializers.brand_serializers import BrandSerializer

class BrandListCreateView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class BrandRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

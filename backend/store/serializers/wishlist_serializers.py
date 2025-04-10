from rest_framework import serializers
from store.models import Wishlist

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'

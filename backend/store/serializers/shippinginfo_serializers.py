from rest_framework import serializers
from store.models import ShippingInfo

class ShippingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingInfo
        fields = '__all__'

from rest_framework import serializers
from models import *

class LineItemSerializer(serializers.ModelSerializer):
    product = serializers.Field(source='product.title')
    class Meta:
        model = LineItem
        fields = ('product', 'unit_price', 'quantity')

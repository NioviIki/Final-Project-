from rest_framework import serializers
from .models import Order
class OrderSerializer(serializers.ModelSerializer):
    order_item = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'delivery_adress', 'status', 'user_id', 'order_item', 'user_email']
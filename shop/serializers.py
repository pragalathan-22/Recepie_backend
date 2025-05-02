

from rest_framework import serializers
from .models import CompanyInfo, FoodItem, Order, OrderItem,Transaction

class CompanyInfoSerializer(serializers.ModelSerializer):
    logoUrl = serializers.SerializerMethodField()

    class Meta:
        model = CompanyInfo
        fields = ['name', 'logo', 'logoUrl']

    def get_logoUrl(self, obj):
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None

class FoodSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'rate', 'image','subcategory']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class OrderItemSerializer(serializers.ModelSerializer):
    food_item = FoodSerializer()

    class Meta:
        model = OrderItem
        fields = ['food_item', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer_name', 'customer_phone',
            'total_amount', 'status', 'created_at', 'updated_at',
            'notes', 'items'
        ]

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'amount', 'status']

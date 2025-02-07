from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('id', 'total_price')

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        order.total_price = sum(item['price'] for item in validated_data.get('items', []))
        order.save()
        return order

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.total_price = sum(item['price'] for item in validated_data.get('items', []))
        instance.save(update_fields=['table_number', 'items', 'status', 'total_price'])
        return instance

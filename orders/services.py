from .models import Order


class OrderService:
    @staticmethod
    def create_order(data):
        order = Order.objects.create(**data)
        return order

    @staticmethod
    def update_order(order_id, data):
        order = Order.objects.get(id=order_id)
        for key, value in data.items():
            setattr(order, key, value)
        order.save()
        return order

    @staticmethod
    def delete_order(order_id):
        order = Order.objects.get(id=order_id)
        order.delete()
        return True

    @staticmethod
    def calculate_revenue():
        return sum(order.total_price for order in Order.objects.filter(status='paid'))

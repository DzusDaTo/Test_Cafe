from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Order


class OrderAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.order_data = {
            "table_number": 9,
            "items": [{"name": "Салат", "price": 250}, {"name": "Чай", "price": 100}],
        }
        self.order = Order.objects.create(**self.order_data)

    def test_get_orders(self):
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_order(self):
        new_order_data = {
            "table_number": 10,
            "items": [{"name": "Паста", "price": 300}],
        }
        response = self.client.post('/api/orders/', new_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['table_number'], 6)

    def test_update_order(self):
        updated_data = {
            "table_number": 10,
            "items": [{"name": "Сок", "price": 200}],
        }
        response = self.client.put(f'/api/orders/{self.order.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['table_number'], 10)

    def test_delete_order(self):
        response = self.client.delete(f'/api/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())


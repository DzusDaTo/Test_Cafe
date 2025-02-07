from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from rest_framework.views import exception_handler


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['error'] = str(exc)
    return response

from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from .forms import OrderForm
from .services import OrderService
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from typing import List, Dict, Any, Optional


# Добавление заказа
def add_order(request: HttpRequest) -> HttpResponse:
    form: Optional[OrderForm] = None

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            table_number: int = form.cleaned_data['table_number']
            status: str = form.cleaned_data['status']
            items_input: str = form.cleaned_data['items']

            try:
                items: List[Dict[str, Any]] = []
                for item_str in items_input.split(','):
                    name, price = item_str.split('-')
                    items.append({
                        'name': name.strip(),
                        'price': float(price.strip())
                    })
            except ValueError:
                return HttpResponseBadRequest("Некорректный формат ввода блюд и цен.")

            try:
                order: Order = Order.objects.create(
                    table_number=table_number,
                    items=items,
                    status=status
                )
            except ValidationError as e:
                return HttpResponseBadRequest(str(e))

            return redirect('order_list')
    else:
        form = OrderForm()

    return render(request, 'orders/order_create.html', {'form': form})


# Обновление заказа
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            OrderService.update_order(order_id, form.cleaned_data)
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/order_edit.html', {'form': form, 'order': order})


# Удаление заказа
def delete_order(request: HttpRequest, order_id: int) -> HttpResponse:
    if request.method == 'POST':
        OrderService.delete_order(order_id)
        return redirect('order_list')
    order: Order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_delete_confirm.html', {'order': order})


# Список заказов
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list_view.html', {'orders': orders})


# Расчет выручки
def calculate_revenue(request):
    revenue = OrderService.calculate_revenue()
    return render(request, 'orders/order_revenue_view.html', {'revenue': revenue})


STATUS_CHOICES = [
    ('pending', 'В ожидании'),
    ('ready', 'Готово'),
    ('paid', 'Оплачено'),
]


# Поиск
def search_order(request):
    search_query = request.GET.get('search_query', '')
    if search_query:
        status_map = {v: k for k, v in dict(STATUS_CHOICES).items()}

        if search_query in status_map:
            search_query_status = status_map[search_query]
            orders = Order.objects.filter(
                Q(table_number__icontains=search_query) | Q(status=search_query_status)
            )
        else:
            orders = Order.objects.filter(
                Q(table_number__icontains=search_query) | Q(status__icontains=search_query)
            )
    else:
        orders = Order.objects.none()

    return render(request, 'orders/order_search.html', {'orders': orders, 'search_query': search_query})
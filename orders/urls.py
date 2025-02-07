from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('add/', views.add_order, name='add_order'),
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('search/', views.search_order, name='search_order'),
    path('update_status/<int:order_id>/', views.update_order, name='update_order'),
    path('revenue/', views.calculate_revenue, name='calculate_revenue'),
]

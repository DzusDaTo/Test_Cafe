from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'items', 'status']
        widgets = {
            'status': forms.Select(choices=Order.STATUS_CHOICES),
        }

    table_number = forms.IntegerField(required=True, label='Номер стола')

    items = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Введите блюда и цену в формате: Блюдо1 - 100, Блюдо2 - 150'}), label='Блюда и цены')

    status = forms.ChoiceField(choices=Order.STATUS_CHOICES, initial='pending', label='Статус')

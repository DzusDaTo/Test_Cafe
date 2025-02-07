from django.core.exceptions import ValidationError
from django.db import models


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.IntegerField()
    items = models.JSONField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def clean(self):
        if self.table_number <= 0:
            raise ValidationError("Номер столика должен быть положительным числом.")

        if self.__class__.objects.filter(table_number=self.table_number, status__in=['pending', 'ready']).exists():
            raise ValidationError(f"Столик №{self.table_number} уже занят заказом.")

    def save(self, *args, **kwargs):
        self.full_clean()
        if isinstance(self.items, str):
            try:
                self.items = eval(self.items)
            except Exception as e:
                raise ValueError(f"Некорректный формат данных в 'items': {e}")

        if isinstance(self.items, list):
            self.total_price = sum(
                item.get('price', 0) * item.get('quantity', 1)
                for item in self.items if isinstance(item, dict) and 'price' in item
            )
        else:
            self.total_price = 0.00

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Заказ {self.id} для стола {self.table_number}'

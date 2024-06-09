# inventory/models.py
from django.db import models

class Employee(models.Model):
    POSITION_CHOICES = [
        ('general_director', 'Генеральный директор'),
        ('chief_accountant', 'Главный бухгалтер'),
        ('storekeeper', 'Кладовщик'),
        ('executive_director', 'Исполнительный директор'),
    ]
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)

    def __str__(self):
        return f'{self.name} ({self.position})'

class Material(models.Model):
    name = models.CharField(max_length=255)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class WriteOffAct(models.Model):
    date = models.DateField()
    chief_accountant = models.ForeignKey(Employee, related_name='acts_as_chief_accountant', on_delete=models.SET_NULL, null=True)
    storekeeper = models.ForeignKey(Employee, related_name='acts_as_storekeeper', on_delete=models.SET_NULL, null=True)
    executive_director = models.ForeignKey(Employee, related_name='acts_as_executive_director', on_delete=models.SET_NULL, null=True)
    general_director = models.ForeignKey(Employee, related_name='acts_as_general_director', on_delete=models.SET_NULL, null=True)

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())

class WriteOffItem(models.Model):
    act = models.ForeignKey(WriteOffAct, related_name='items', on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    reason = models.CharField(max_length=255)

    @property
    def total_price(self):
        return self.material.price_per_unit * self.quantity

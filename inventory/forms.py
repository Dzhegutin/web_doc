from django import forms
from .models import WriteOffAct, WriteOffItem, Employee

class WriteOffActForm(forms.ModelForm):
    class Meta:
        model = WriteOffAct
        fields = ['date', 'chief_accountant', 'storekeeper', 'executive_director', 'general_director']
        labels = {
            'date': 'Дата:',
            'chief_accountant': 'Главный бухгалтер:',
            'storekeeper': 'Кладовщик:',
            'executive_director': 'Исполнительный директор:',
            'general_director': 'Генеральный директор:',
        }

class WriteOffItemForm(forms.ModelForm):
    class Meta:
        model = WriteOffItem
        fields = ['material', 'quantity', 'reason']
        labels = {
            'material': 'Материал:',
            'quantity': 'Количество:',
            'reason': 'Причина списания:',
        }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'position']
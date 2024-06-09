# inventory/admin.py
from django.contrib import admin
from .models import Employee, Material, WriteOffAct, WriteOffItem

admin.site.register(Employee)
admin.site.register(Material)
admin.site.register(WriteOffAct)
admin.site.register(WriteOffItem)

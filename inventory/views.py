# inventory/views.py
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import WriteOffAct, WriteOffItem, Material, Employee
from .forms import WriteOffActForm, WriteOffItemForm
from django.urls import reverse

def index(request):
    return render(request, 'inventory/index.html')

def create_writeoff_act(request):
    if request.method == 'POST':
        act_form = WriteOffActForm(request.POST)
        item_form = WriteOffItemForm(request.POST)
        if act_form.is_valid():
            act = act_form.save()
            for material_id, quantity, reason in zip(
                    request.POST.getlist('material'),
                    request.POST.getlist('quantity'),
                    request.POST.getlist('reason'),
            ):
                WriteOffItem.objects.create(
                    act=act,
                    material_id=material_id,
                    quantity=quantity,
                    reason=reason,
                )
            return redirect('list_writeoff_acts')
    else:
        act_form = WriteOffActForm()
        item_form = WriteOffItemForm()
    employees = Employee.objects.all()
    materials = Material.objects.all()

    return render(request, 'inventory/create_writeoff_act.html', {
        'act_form': act_form,
        'item_form': item_form,
        'employees': employees,
        'materials': materials,
    })

def list_writeoff_acts(request):
    acts = WriteOffAct.objects.all()
    return render(request, 'inventory/list_writeoff_acts.html', {'acts': acts})

def manage_materials(request):
    if request.method == 'POST':
        print(request.POST)
        if 'name' in request.POST and 'price_per_unit' in request.POST:
            # Обработка формы для добавления материала
            name = request.POST['name']
            price_per_unit = request.POST['price_per_unit']
            Material.objects.create(name=name, price_per_unit=price_per_unit)
            return redirect('manage_materials')
        elif 'employee_name' in request.POST and 'employee_position' in request.POST:

            # Обработка формы для добавления сотрудника
            name = request.POST['employee_name']
            position = request.POST['employee_position']
            print(position, name)
            Employee.objects.create(name=name, position=position)
            return redirect('manage_materials')

    materials = Material.objects.all()
    employees = Employee.objects.all()
    positions = list(map(lambda x: x[1], Employee.POSITION_CHOICES))

    return render(request, 'inventory/manage_materials.html', {'materials': materials,
                                                               'employees': employees,
                                                               'positions': positions,
                                                              })
def delete_act(request, act_id):
    act = get_object_or_404(WriteOffAct, id=act_id)
    WriteOffItem.objects.filter(act=act).delete()
    act.delete()
    return redirect('list_writeoff_acts')


def delete_employee(request, e_id):
    employee = get_object_or_404(Employee, id=e_id)

    # Проверка и обработка связанных актов списания
    WriteOffAct.objects.filter(
        models.Q(chief_accountant=employee) |
        models.Q(storekeeper=employee) |
        models.Q(executive_director=employee) |
        models.Q(general_director=employee)
    ).update(chief_accountant=None, storekeeper=None, executive_director=None, general_director=None)

    employee.delete()
    return redirect('manage_materials')


def delete_material(request, m_id):
    material = get_object_or_404(Material, id=m_id)
    write_off_items = WriteOffItem.objects.filter(material=material)
    write_off_acts = WriteOffAct.objects.filter(items__in=write_off_items).distinct()

    write_off_items.delete()


    for act in write_off_acts:
        if not act.items.exists():
            act.delete()

    material.delete()

    return redirect('manage_materials')


def print_act(request, act_id):
    act = get_object_or_404(WriteOffAct, id=act_id)
    items = WriteOffItem.objects.filter(act=act)
    total_sum = sum(item.total_price for item in items)
    return render(request, 'inventory/print_act.html', {
        'act': act,
        'items': items,
        'total_sum': total_sum,
    })


def edit_writeoff_act(request, act_id):

    act = get_object_or_404(WriteOffAct, pk=act_id)
    empl = WriteOffAct.objects.filter(pk=act_id)
    products = WriteOffItem.objects.filter(act_id=act_id)
    total_sum = sum(product.quantity * product.material.price_per_unit for product in products)

    if request.method == 'POST':
        act_form = WriteOffActForm(request.POST, instance=act)
        item_form = WriteOffItemForm(request.POST)
        if act_form.is_valid():
            act = act_form.save()
            for material_id, quantity, reason in zip(
                    request.POST.getlist('material'),
                    request.POST.getlist('quantity'),
                    request.POST.getlist('reason'),
            ):
                WriteOffItem.objects.update(
                    act=act,
                    material_id=material_id,
                    quantity=quantity,
                    reason=reason,
                )
            return redirect('list_writeoff_acts')
    else:

        act_form = WriteOffActForm(instance=act)
        item_form = WriteOffItemForm()
        print(products.values())
        print(act_id)
    return render(request, 'inventory/edit_writeoff_act.html', {
        'act_form': act_form,
        'item_form': item_form,
        'empl': empl,
        'products': products,
        'total_sum': total_sum
    })

def get_material_price(request):
    material_id = request.GET.get('material_id')
    try:
        material = Material.objects.get(id=material_id)
        price = material.price_per_unit
        return JsonResponse({'price': price}, safe=False)
    except Material.DoesNotExist:
        return JsonResponse({'error': 'Material not found'}, status=404)
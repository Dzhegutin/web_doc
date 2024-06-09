from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_writeoff_act, name='create_writeoff_act'),
    path('list/', views.list_writeoff_acts, name='list_writeoff_acts'),
    path('materials/', views.manage_materials, name='manage_materials'),

    path('delete_act/<int:act_id>/', views.delete_act, name='delete_act'),
    path('delete_employee/<int:e_id>/', views.delete_employee, name='delete_employee'),
    path('delete_material/<int:m_id>/', views.delete_material, name='delete_material'),


    path('print-act/<int:act_id>/', views.print_act, name='print_act'),

    path('edit/<int:act_id>/', views.edit_writeoff_act, name='edit_writeoff_act'),
    path('get-material-price/', views.get_material_price, name='get_material_price'),
]

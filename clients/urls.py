from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.client_list, name='client_list'),
    path('create/', views.client_create, name='client_create'),
    path('<int:pk>/', views.client_detail, name='client_detail'),
    path('<int:pk>/update/', views.client_update, name='client_update'),
    path('export/csv/', views.export_clients_csv, name='export_clients_csv'),
    path('export/xlsx/', views.export_clients_xlsx, name='export_clients_xlsx'),
]
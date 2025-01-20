from django.urls import path
from . import views

app_name = 'treks'  # Add this namespace

urlpatterns = [
    path('expense/print/<int:pk>/', views.print_expense, name='print_expense'),
    path('expense/pdf/<int:pk>/', views.download_expense_pdf, name='download_expense_pdf'),
]
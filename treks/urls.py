from django.urls import path
from . import views

app_name = 'treks'

urlpatterns = [
    path('expense/print/<int:pk>/', views.print_expense, name='print_expense'),
    path('expense/pdf/<int:pk>/', views.download_expense_pdf, name='download_expense_pdf'),
    path('trekkingexpense/<int:pk>/guide_porter_print/', views.guide_porter_print, name='guide_porter_print'),
]
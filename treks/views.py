from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.shortcuts import get_object_or_404, render
from .models import TrekkingExpense
from django.template.loader import render_to_string

def print_expense(request, pk):
    expense = get_object_or_404(TrekkingExpense, pk=pk)
    # Create list of expenses in order
    expense_list = []
    current_sn = 1

    # Add regular expenses only if they exist
    if expense.package_rate:
        expense_list.append({
            'sn': current_sn,
            'particular': 'Package for Members',
            'rate': expense.package_rate,
            'numbers': expense.package_numbers,
            'days': expense.package_days,
            'total': expense.package_total,
            'remarks': ''
        })
        current_sn += 1

    if expense.guide_salary_rate:
        expense_list.append({
            'sn': current_sn,
            'particular': 'Salary for Trekking Guide',
            'rate': expense.guide_salary_rate,
            'numbers': 1,
            'days': expense.guide_salary_days,
            'total': expense.guide_salary_total,
            'remarks': ''
        })
        current_sn += 1

    if expense.assistant_guide_salary_rate:
        expense_list.append({
            'sn': current_sn,
            'particular': 'Salary for Assistant Guide',
            'rate': expense.assistant_guide_salary_rate,
            'numbers': 1,
            'days': expense.assistant_guide_days,
            'total': expense.assistant_guide_salary_total,
            'remarks': ''
        })
        current_sn += 1

    if expense.porter_salary_rate:
        expense_list.append({
            'sn': current_sn,
            'particular': 'Salary for Porter',
            'rate': expense.porter_salary_rate,
            'numbers': expense.porter_numbers,
            'days': expense.porter_days,
            'total': expense.porter_salary_total,
            'remarks': ''
        })
        current_sn += 1

    # Add additional expenses
    for add_expense in expense.additional_expenses.all():
        expense_list.append({
            'sn': current_sn,
            'particular': add_expense.particular,
            'rate': add_expense.rate,
            'numbers': add_expense.numbers,
            'days': add_expense.days,
            'total': add_expense.total_amount,
            'remarks': add_expense.remarks
        })
        current_sn += 1

    return render(request, 'treks/print_expense.html', {
        'expense': expense,
        'expense_list': expense_list,
    })

def download_expense_pdf(request, pk):
    expense = get_object_or_404(TrekkingExpense, pk=pk)
    # Build expense_list exactly as in print_expense
    expense_list = []
    current_sn = 1

    if expense.package_rate:
        expense_list.append({
            'sn': current_sn,
            'particular': 'Package for Members',
            'rate': expense.package_rate,
            'numbers': expense.package_numbers,
            'days': expense.package_days,
            'total': expense.package_total,
            'remarks': ''
        })
        current_sn += 1

    if expense.guide_salary_rate:
        expense_list.append({
            'sn': current_sn,
            'particular': 'Salary for Trekking Guide',
            'rate': expense.guide_salary_rate,
            'numbers': 1,
            'days': expense.guide_salary_days,
            'total': expense.guide_salary_total,
            'remarks': ''
        })
        current_sn += 1

    if expense.assistant_guide_salary_rate:
        expense_list.append({
            'sn': current_sn,
            'particular': 'Salary for Assistant Guide',
            'rate': expense.assistant_guide_salary_rate,
            'numbers': 1,
            'days': expense.assistant_guide_days,
            'total': expense.assistant_guide_salary_total,
            'remarks': ''
        })
        current_sn += 1

    if expense.porter_salary_rate:
        expense_list.append({
            'sn': current_sn,
            'particular': 'Salary for Porter',
            'rate': expense.porter_salary_rate,
            'numbers': expense.porter_numbers,
            'days': expense.porter_days,
            'total': expense.porter_salary_total,
            'remarks': ''
        })
        current_sn += 1

    for add_expense in expense.additional_expenses.all():
        expense_list.append({
            'sn': current_sn,
            'particular': add_expense.particular,
            'rate': add_expense.rate,
            'numbers': add_expense.numbers,
            'days': add_expense.days,
            'total': add_expense.total_amount,
            'remarks': add_expense.remarks
        })
        current_sn += 1

    html = render_to_string('treks/print_expense.html', {
        'expense': expense,
        'expense_list': expense_list,
    })
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="expense_{pk}.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response

def guide_porter_print(request, pk):
    expense = get_object_or_404(TrekkingExpense, pk=pk)
    return render(request, 'treks/guide_porter_print.html', {
        'expense': expense,
    })
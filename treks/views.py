from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.shortcuts import get_object_or_404, render
from .models import TrekkingExpense

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
    # Create list of expenses in order (same as print_expense)
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

    template = get_template('treks/print_expense.html')
    html = template.render({
        'expense': expense,
        'expense_list': expense_list,
    })
    
    # Create PDF
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="trek_expense_{expense.pk}.pdf"'
        return response
    
    return HttpResponse('Error generating PDF', status=400)